"""
Enterprise-grade Prometheus metrics for the Payments API.

This module provides standardized Prometheus metrics following
best practices for production observability.
"""

import logging
import time
from typing import Any

from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Histogram
from prometheus_client import Info
from prometheus_client import generate_latest
from prometheus_client.core import CollectorRegistry

logger = logging.getLogger(__name__)

# Create a custom registry for our metrics
registry = CollectorRegistry()

# Application info metric
app_info = Info(
    "payments_api_build", "Application build information", registry=registry
)

# HTTP Request metrics with canonical labels
http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests processed",
    ["method", "endpoint", "status_code"],
    registry=registry,
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
    buckets=(
        0.005,
        0.01,
        0.025,
        0.05,
        0.075,
        0.1,
        0.25,
        0.5,
        0.75,
        1.0,
        2.5,
        5.0,
        7.5,
        10.0,
    ),
    registry=registry,
)

http_request_size_bytes = Histogram(
    "http_request_size_bytes",
    "HTTP request size in bytes",
    ["method", "endpoint"],
    registry=registry,
)

# Webhook-specific metrics
webhook_events_total = Counter(
    "webhook_events_total",
    "Total webhook events received",
    ["provider", "event_type", "status"],
    registry=registry,
)

webhook_processing_duration_seconds = Histogram(
    "webhook_processing_duration_seconds",
    "Time spent processing webhook events",
    ["provider", "event_type"],
    buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0),
    registry=registry,
)

webhook_signature_validations_total = Counter(
    "webhook_signature_validations_total",
    "Total webhook signature validations",
    ["provider", "valid"],
    registry=registry,
)

# Database metrics
database_operations_total = Counter(
    "database_operations_total",
    "Total database operations",
    ["operation", "table", "status"],
    registry=registry,
)

database_operation_duration_seconds = Histogram(
    "database_operation_duration_seconds",
    "Database operation duration in seconds",
    ["operation", "table"],
    registry=registry,
)

database_connections_active = Gauge(
    "database_connections_active",
    "Number of active database connections",
    registry=registry,
)

# Background job metrics
job_runs_total = Counter(
    "job_runs_total",
    "Total background job runs",
    ["job_name", "status"],
    registry=registry,
)

job_duration_seconds = Histogram(
    "job_duration_seconds",
    "Background job execution duration",
    ["job_name"],
    buckets=(1, 5, 10, 30, 60, 300, 600, 1800, 3600),
    registry=registry,
)

# DLQ metrics
dlq_messages_total = Counter(
    "dlq_messages_total",
    "Total messages in dead letter queue",
    ["action"],  # added, retried, failed
    registry=registry,
)

dlq_messages_pending = Gauge(
    "dlq_messages_pending", "Number of pending messages in DLQ", registry=registry
)

# Reconciliation metrics
reconciliation_events_processed_total = Counter(
    "reconciliation_events_processed_total",
    "Total events processed during reconciliation",
    ["provider"],
    registry=registry,
)

reconciliation_anomalies_detected_total = Counter(
    "reconciliation_anomalies_detected_total",
    "Total anomalies detected during reconciliation",
    ["anomaly_type"],
    registry=registry,
)

reconciliation_last_run_timestamp = Gauge(
    "reconciliation_last_run_timestamp",
    "Timestamp of last reconciliation run",
    registry=registry,
)

# Application health metrics
application_up = Gauge(
    "application_up", "Application health status (1=up, 0=down)", registry=registry
)

application_ready = Gauge(
    "application_ready",
    "Application readiness status (1=ready, 0=not ready)",
    registry=registry,
)

# Initialize application info
app_info.info(
    {"version": "0.2.0-rc", "name": "payments-api", "environment": "production"}
)

# Set initial health status
application_up.set(1)


class MetricsCollector:
    """
    Utility class to collect and expose metrics in Prometheus format.

    Provides methods to record metrics throughout the application
    with proper labeling and timing.
    """

    @staticmethod
    def record_http_request(
        method: str, endpoint: str, status_code: int, duration: float, size: int = 0
    ):
        """Record HTTP request metrics."""
        http_requests_total.labels(
            method=method, endpoint=endpoint, status_code=str(status_code)
        ).inc()

        http_request_duration_seconds.labels(method=method, endpoint=endpoint).observe(
            duration
        )

        if size > 0:
            http_request_size_bytes.labels(method=method, endpoint=endpoint).observe(
                size
            )

    @staticmethod
    def record_webhook_event(
        provider: str, event_type: str, status: str, duration: float = None
    ):
        """Record webhook processing metrics."""
        webhook_events_total.labels(
            provider=provider, event_type=event_type, status=status
        ).inc()

        if duration is not None:
            webhook_processing_duration_seconds.labels(
                provider=provider, event_type=event_type
            ).observe(duration)

    @staticmethod
    def record_signature_validation(provider: str, valid: bool):
        """Record webhook signature validation."""
        webhook_signature_validations_total.labels(
            provider=provider, valid=str(valid).lower()
        ).inc()

    @staticmethod
    def record_database_operation(
        operation: str, table: str, status: str, duration: float = None
    ):
        """Record database operation metrics."""
        database_operations_total.labels(
            operation=operation, table=table, status=status
        ).inc()

        if duration is not None:
            database_operation_duration_seconds.labels(
                operation=operation, table=table
            ).observe(duration)

    @staticmethod
    def record_job_run(job_name: str, status: str, duration: float = None):
        """Record background job metrics."""
        job_runs_total.labels(job_name=job_name, status=status).inc()

        if duration is not None:
            job_duration_seconds.labels(job_name=job_name).observe(duration)

    @staticmethod
    def record_dlq_message(action: str):
        """Record DLQ message action."""
        dlq_messages_total.labels(action=action).inc()

    @staticmethod
    def set_dlq_pending_count(count: int):
        """Set current DLQ pending message count."""
        dlq_messages_pending.set(count)

    @staticmethod
    def record_reconciliation_events(provider: str, count: int):
        """Record reconciliation event processing."""
        reconciliation_events_processed_total.labels(provider=provider).inc(count)

    @staticmethod
    def record_reconciliation_anomaly(anomaly_type: str):
        """Record reconciliation anomaly detection."""
        reconciliation_anomalies_detected_total.labels(anomaly_type=anomaly_type).inc()

    @staticmethod
    def set_reconciliation_last_run():
        """Update reconciliation last run timestamp."""
        reconciliation_last_run_timestamp.set(time.time())

    @staticmethod
    def set_application_ready(ready: bool):
        """Set application readiness status."""
        application_ready.set(1 if ready else 0)

    @staticmethod
    def set_database_connections(count: int):
        """Set active database connection count."""
        database_connections_active.set(count)

    @staticmethod
    def get_prometheus_metrics() -> str:
        """Generate Prometheus metrics output."""
        return generate_latest(registry).decode("utf-8")


# Context manager for timing operations
class MetricsTimer:
    """Context manager for timing operations with automatic metric recording."""

    def __init__(self, metric_recorder, *args, **kwargs):
        self.metric_recorder = metric_recorder
        self.args = args
        self.kwargs = kwargs
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        duration = time.time() - self.start_time
        self.metric_recorder(*self.args, duration=duration, **self.kwargs)


# Global metrics collector instance
metrics = MetricsCollector()


def get_metrics_summary() -> dict[str, Any]:
    """
    Get a summary of current metrics for health checks and debugging.

    Returns:
        Dictionary containing metric summaries
    """
    return {
        "http_requests_total": http_requests_total._value._value,
        "webhook_events_total": webhook_events_total._value._value,
        "database_operations_total": database_operations_total._value._value,
        "job_runs_total": job_runs_total._value._value,
        "dlq_messages_pending": dlq_messages_pending._value._value,
        "application_up": application_up._value._value,
        "application_ready": application_ready._value._value,
        "last_updated": time.time(),
    }
