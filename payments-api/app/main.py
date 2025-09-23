import asyncio
import logging
import time
import uuid
from contextlib import asynccontextmanager
from datetime import UTC
from datetime import datetime

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Query
from fastapi import Request
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.config import get_settings
from app.config import settings_dep
from app.db import db_manager
from app.db import get_db
from app.jobs.reconciliation import reconciliation_job
from app.jobs.retry_worker import retry_worker
from app.metrics import MetricsTimer
from app.metrics import metrics
from app.models import PaymentEvent
from app.schemas import HealthResponse
from app.schemas import MetricsResponse
from app.schemas import ReadinessResponse
from app.schemas import ReconciliationSummary
from app.schemas import WebhookResponse
from app.utils.ports import get_app_port
from app.webhooks.paypal import process_paypal_webhook
from app.webhooks.stripe import process_stripe_webhook


# Configure logging with trace_id support
class TraceFormatter(logging.Formatter):
    """Custom formatter that includes trace_id and request_id when available."""

    def format(self, record):
        trace_id = getattr(record, "trace_id", None)
        request_id = getattr(record, "request_id", None)

        if trace_id:
            record.trace_id_fmt = f" [trace_id={trace_id}]"
        else:
            record.trace_id_fmt = ""

        if request_id:
            record.request_id_fmt = f" [request_id={request_id}]"
        else:
            record.request_id_fmt = ""

        return super().format(record)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s%(trace_id_fmt)s%(request_id_fmt)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("payments-api.log")],
)

# Set custom formatter
for handler in logging.getLogger().handlers:
    handler.setFormatter(
        TraceFormatter(
            "%(asctime)s - %(name)s - %(levelname)s%(trace_id_fmt)s%(request_id_fmt)s - %(message)s"
        )
    )

logger = logging.getLogger(__name__)

# Legacy metrics for JSON endpoint (deprecated - use Prometheus /metrics)
metrics_counters: dict[str, int] = {
    "webhooks_received": 0,
    "webhooks_processed": 0,
    "webhooks_duplicate": 0,
    "webhooks_invalid_signature": 0,
    "webhooks_failed": 0,
    "dlq_messages_added": 0,
    "dlq_messages_retried": 0,
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    settings = get_settings()

    # Log startup
    logger.info("Starting Payments API", extra=settings.get_masked_config())

    # Create database tables
    await db_manager.create_tables()
    logger.info("Database tables created/verified")

    # Start background workers
    retry_worker_task = asyncio.create_task(retry_worker.start())
    logger.info("Background workers started")

    yield

    # Cleanup
    await retry_worker.stop()
    retry_worker_task.cancel()
    await db_manager.close()
    logger.info("Payments API shutdown complete")


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create FastAPI app with optional settings override for testing."""

    app = FastAPI(
        title="Payments Reliability API",
        description="Production-grade webhook processing service for Stripe and PayPal",
        version="0.2.0-rc",
        lifespan=lifespan,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add request size limiting middleware
    @app.middleware("http")
    async def request_size_limit_middleware(request: Request, call_next):
        """Limit request body size to prevent DoS attacks."""
        content_length = request.headers.get("content-length")
        if content_length:
            try:
                size = int(content_length)
                max_size = get_settings().max_request_size
                if size > max_size:
                    return Response(
                        content=f'{{"detail":"Request body too large. Maximum size: {max_size} bytes"}}',
                        status_code=413,
                        media_type="application/json",
                    )
            except ValueError:
                pass  # Invalid content-length header, let the request proceed

        return await call_next(request)

    # Add request logging middleware with tracing
    @app.middleware("http")
    async def request_logging_middleware(request: Request, call_next):
        """Log all requests with timing and trace propagation."""
        start_time = time.time()

        # Generate request_id and extract trace_id if present
        request_id = str(uuid.uuid4())[:8]
        trace_id = (
            request.headers.get("x-trace-id")
            or request.headers.get("traceparent", "").split("-")[1]
            if "traceparent" in request.headers
            else None
        )

        # Store in request state for access in handlers
        request.state.request_id = request_id
        request.state.trace_id = trace_id

        response = await call_next(request)

        end_time = time.time()
        duration = end_time - start_time

        # Create log record with trace context
        log_extra = {
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_seconds": duration,
            "user_agent": request.headers.get("user-agent", ""),
            "content_length": request.headers.get("content-length", 0),
            "request_id": request_id,
        }

        if trace_id:
            log_extra["trace_id"] = trace_id

        logger.info(
            f"{request.method} {request.url.path} - {response.status_code}",
            extra=log_extra,
        )

        # Record metrics
        endpoint = request.url.path
        metrics.record_http_request(
            method=request.method,
            endpoint=endpoint,
            status_code=response.status_code,
            duration=duration,
            size=int(request.headers.get("content-length", 0))
            if request.headers.get("content-length", "0").isdigit()
            else 0,
        )

        # Add trace headers to response
        if trace_id:
            response.headers["x-trace-id"] = trace_id
        response.headers["x-request-id"] = request_id

        return response

    # Add routes
    _add_routes(app)

    # Override settings if provided (for testing)
    if settings:
        app.dependency_overrides[settings_dep] = lambda: settings

    return app


def _add_routes(app: FastAPI) -> None:
    """Add all routes to the FastAPI app."""

    # Webhook endpoints
    @app.post("/webhooks/stripe", response_model=WebhookResponse)
    async def stripe_webhook(
        request: Request,
        db: AsyncSession = Depends(get_db),
        settings: Settings = Depends(settings_dep),
    ):
        """
        Process Stripe webhook with signature verification.

        Validates webhook signature using Stripe's official scheme,
        ensures idempotency, and persists event data.
        """
        start_time = time.time()
        try:
            metrics_counters["webhooks_received"] += 1
            result = await process_stripe_webhook(request, db, settings)

            # Record metrics based on result
            if result.message == "processed":
                metrics_counters["webhooks_processed"] += 1
                metrics.record_webhook_event(
                    "stripe", "webhook", "processed", time.time() - start_time
                )
            elif result.message == "duplicate ignored":
                metrics_counters["webhooks_duplicate"] += 1
                metrics.record_webhook_event(
                    "stripe", "webhook", "duplicate", time.time() - start_time
                )

            return result

        except HTTPException as e:
            if e.status_code == 400 and "signature" in e.detail:
                metrics_counters["webhooks_invalid_signature"] += 1
                metrics.record_signature_validation("stripe", False)
            else:
                metrics_counters["webhooks_failed"] += 1
                metrics.record_webhook_event(
                    "stripe", "webhook", "failed", time.time() - start_time
                )
            raise
        except Exception as e:
            metrics_counters["webhooks_failed"] += 1
            metrics.record_webhook_event(
                "stripe", "webhook", "error", time.time() - start_time
            )
            logger.error(f"Unexpected error in Stripe webhook: {e}")
            raise HTTPException(
                status_code=500, detail="Internal server error"
            ) from None

    @app.post("/webhooks/paypal", response_model=WebhookResponse)
    async def paypal_webhook(
        request: Request,
        db: AsyncSession = Depends(get_db),
        settings: Settings = Depends(settings_dep),
    ):
        """
        Process PayPal webhook with signature verification.

        Supports both real PayPal verification API and demo HMAC mode
        for development. Ensures idempotency and persists event data.
        """
        start_time = time.time()
        try:
            metrics_counters["webhooks_received"] += 1
            result = await process_paypal_webhook(request, db, settings)

            # Record metrics based on result
            if result.message == "processed":
                metrics_counters["webhooks_processed"] += 1
                metrics.record_webhook_event(
                    "paypal", "webhook", "processed", time.time() - start_time
                )
            elif result.message == "duplicate ignored":
                metrics_counters["webhooks_duplicate"] += 1
                metrics.record_webhook_event(
                    "paypal", "webhook", "duplicate", time.time() - start_time
                )

            return result

        except HTTPException as e:
            if e.status_code == 400 and "signature" in e.detail:
                metrics_counters["webhooks_invalid_signature"] += 1
                metrics.record_signature_validation("paypal", False)
            else:
                metrics_counters["webhooks_failed"] += 1
                metrics.record_webhook_event(
                    "paypal", "webhook", "failed", time.time() - start_time
                )
            raise
        except Exception as e:
            metrics_counters["webhooks_failed"] += 1
            metrics.record_webhook_event(
                "paypal", "webhook", "error", time.time() - start_time
            )
            logger.error(f"Unexpected error in PayPal webhook: {e}")
            raise HTTPException(
                status_code=500, detail="Internal server error"
            ) from None

    # Health and monitoring endpoints
    @app.get("/health", response_model=HealthResponse)
    async def health():
        """Liveness check endpoint."""
        return HealthResponse(
            status="healthy",
            timestamp=datetime.now(UTC),
            version="0.2.0-rc",
        )

    @app.get("/ready", response_model=ReadinessResponse)
    async def readiness():
        """Readiness check endpoint with dependency checks."""
        checks = {"database": await db_manager.health_check()}

        all_healthy = all(checks.values())

        # Update metrics
        metrics.set_application_ready(all_healthy)

        return ReadinessResponse(
            status="ready" if all_healthy else "not_ready",
            checks=checks,
            timestamp=datetime.now(UTC),
        )

    @app.get("/metrics")
    async def prometheus_metrics():
        """Prometheus metrics endpoint."""
        from fastapi import Response

        return Response(
            content=metrics.get_prometheus_metrics(), media_type="text/plain"
        )

    @app.get("/metrics/json", response_model=MetricsResponse)
    async def json_metrics():
        """JSON metrics endpoint for debugging."""
        return MetricsResponse(
            counters=metrics_counters.copy(),
            timestamp=datetime.now(UTC),
        )

    # Reconciliation endpoint
    @app.get("/reconciliation/summary", response_model=ReconciliationSummary)
    async def reconciliation_summary(
        hours_back: int = Query(24, ge=1, le=168),  # 1 hour to 1 week
        db: AsyncSession = Depends(get_db),
    ):
        """
            Get reconciliation summary for the specified time window.

        Args:
            hours_back: Number of hours to look back (1-168)

            Returns:
                Reconciliation summary with event counts and anomalies
        """
        try:
            with MetricsTimer(metrics.record_job_run, "reconciliation", "success"):
                summary = await reconciliation_job.run_reconciliation(hours_back)
                metrics.set_reconciliation_last_run()
                return ReconciliationSummary(**summary)
        except Exception as e:
            metrics.record_job_run("reconciliation", "failed")
            logger.error(f"Reconciliation summary failed: {e}")
            raise HTTPException(
                status_code=500, detail="Reconciliation failed"
            ) from None

    # Admin endpoints (for debugging/monitoring)
    @app.get("/admin/events")
    async def list_events(
        provider: str = Query(None),
        limit: int = Query(50, ge=1, le=100),
        db: AsyncSession = Depends(get_db),
    ):
        """List recent payment events for debugging."""
        stmt = (
            select(PaymentEvent).order_by(PaymentEvent.received_at.desc()).limit(limit)
        )

        if provider:
            stmt = stmt.where(PaymentEvent.provider == provider)

        result = await db.execute(stmt)
        events = result.scalars().all()

        return [
            {
                "id": event.id,
                "provider": event.provider,
                "event_id": event.event_id,
                "event_type": event.event_type,
                "received_at": event.received_at,
            }
            for event in events
        ]


# Create the default app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    # Get port from environment or find free one
    port = get_app_port()
    print(f"Starting Payments API on port {port}")

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True if get_settings().app_env == "dev" else False,
    )
