import json
import logging

from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.config import settings_dep
from app.db import get_db
from app.models import PaymentEvent
from app.schemas import StripeWebhookEvent
from app.schemas import WebhookResponse
from app.utils.crypto import verify_stripe_signature
from app.utils.idempotency import ensure_idempotency
from app.utils.idempotency import make_idempotency_key

logger = logging.getLogger(__name__)


async def process_stripe_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(settings_dep),
) -> WebhookResponse:
    """Process Stripe webhook with signature verification and idempotency."""

    # Get raw body and signature header
    body = await request.body()
    signature_header = request.headers.get("stripe-signature", "")

    # Verify signature
    if not verify_stripe_signature(
        payload=body,
        signature_header=signature_header,
        signing_secret=settings.stripe_signing_secret,
        tolerance=settings.stripe_timestamp_tolerance,
    ):
        logger.warning(
            "Invalid Stripe signature",
            extra={
                "signature_header": signature_header[:50] + "..."
                if len(signature_header) > 50
                else signature_header,
                "body_length": len(body),
            },
        )
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Parse JSON payload
    try:
        payload_data = json.loads(body.decode("utf-8"))
        event = StripeWebhookEvent(**payload_data)
    except (json.JSONDecodeError, ValueError) as e:
        logger.error(f"Failed to parse Stripe webhook payload: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON payload") from e

    # Extract required fields
    if not event.id or not event.type:
        logger.error("Missing required fields in Stripe webhook")
        raise HTTPException(status_code=400, detail="Missing required fields")

    # Check idempotency
    idempotency_key = make_idempotency_key("stripe", event.id)
    is_first_attempt = await ensure_idempotency(db, idempotency_key)

    if not is_first_attempt:
        logger.info(f"Duplicate Stripe webhook ignored: {event.id}")
        return WebhookResponse(
            status="ok", message="duplicate ignored", event_id=event.id
        )

    try:
        # Store event
        payment_event = PaymentEvent(
            provider="stripe",
            event_id=event.id,
            event_type=event.type,
            payload_json=body.decode("utf-8"),
        )
        db.add(payment_event)
        await db.commit()

        logger.info(
            f"Successfully processed Stripe webhook: {event.id}",
            extra={
                "event_id": event.id,
                "event_type": event.type,
                "provider": "stripe",
            },
        )

        return WebhookResponse(status="ok", message="processed", event_id=event.id)

    except Exception as e:
        await db.rollback()
        logger.error(
            f"Failed to store Stripe webhook: {e}",
            extra={"event_id": event.id, "event_type": event.type, "error": str(e)},
        )
        # In production, this would go to DLQ
        raise HTTPException(status_code=500, detail="Processing failed") from e
