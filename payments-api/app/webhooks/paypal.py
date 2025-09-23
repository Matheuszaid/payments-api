import json
import logging

import httpx
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.config import settings_dep
from app.db import get_db
from app.models import PaymentEvent
from app.schemas import PayPalWebhookEvent
from app.schemas import WebhookResponse
from app.utils.crypto import verify_demo_hmac
from app.utils.idempotency import ensure_idempotency
from app.utils.idempotency import make_idempotency_key

logger = logging.getLogger(__name__)


async def get_paypal_access_token(client_id: str, client_secret: str, mode: str) -> str:
    """
    Get PayPal access token for webhook verification.

    Args:
        client_id: PayPal client ID
        client_secret: PayPal client secret
        mode: PayPal mode (live, sandbox)

    Returns:
        Access token string

    Raises:
        HTTPException: If unable to get token
    """
    base_url = (
        "https://api.paypal.com" if mode == "live" else "https://api.sandbox.paypal.com"
    )
    url = f"{base_url}/v1/oauth2/token"

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers={
                "Accept": "application/json",
                "Accept-Language": "en_US",
            },
            auth=(client_id, client_secret),
            data="grant_type=client_credentials",
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=500, detail="Failed to get PayPal access token"
            )

        return response.json()["access_token"]


async def verify_paypal_webhook_signature(
    headers: dict[str, str], body: bytes, webhook_id: str, access_token: str, mode: str
) -> bool:
    """
    Verify PayPal webhook signature using PayPal's verification API.

    Args:
        headers: Request headers
        body: Raw request body
        webhook_id: PayPal webhook ID
        access_token: PayPal access token
        mode: PayPal mode (live, sandbox)

    Returns:
        True if signature is valid, False otherwise
    """
    required_headers = [
        "PAYPAL-TRANSMISSION-ID",
        "PAYPAL-TRANSMISSION-TIME",
        "PAYPAL-CERT-URL",
        "PAYPAL-AUTH-ALGO",
        "PAYPAL-TRANSMISSION-SIG",
    ]

    # Check for required headers
    for header in required_headers:
        if header not in headers:
            logger.warning(f"Missing PayPal header: {header}")
            return False

    base_url = (
        "https://api.paypal.com" if mode == "live" else "https://api.sandbox.paypal.com"
    )
    url = f"{base_url}/v1/notifications/verify-webhook-signature"

    verification_data = {
        "transmission_id": headers["PAYPAL-TRANSMISSION-ID"],
        "transmission_time": headers["PAYPAL-TRANSMISSION-TIME"],
        "cert_url": headers["PAYPAL-CERT-URL"],
        "auth_algo": headers["PAYPAL-AUTH-ALGO"],
        "transmission_sig": headers["PAYPAL-TRANSMISSION-SIG"],
        "webhook_id": webhook_id,
        "webhook_event": json.loads(body.decode("utf-8")),
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {access_token}",
                },
                json=verification_data,
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("verification_status") == "SUCCESS"
            else:
                logger.error(f"PayPal verification API error: {response.status_code}")
                return False

    except Exception as e:
        logger.error(f"PayPal verification failed: {e}")
        return False


async def process_paypal_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(settings_dep),
) -> WebhookResponse:
    """
    Process PayPal webhook with signature verification and idempotency.

    Args:
        request: FastAPI request object
        db: Database session

    Returns:
        WebhookResponse indicating processing result

    Raises:
        HTTPException: For invalid signatures or malformed data
    """

    # Get raw body
    body = await request.body()
    headers = dict(request.headers)

    # Parse JSON payload first for validation
    try:
        payload_data = json.loads(body.decode("utf-8"))
        event = PayPalWebhookEvent(**payload_data)
    except (json.JSONDecodeError, ValueError) as e:
        logger.error(f"Failed to parse PayPal webhook payload: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON payload") from e

    # Extract required fields
    if not event.id or not event.event_type:
        logger.error("Missing required fields in PayPal webhook")
        raise HTTPException(status_code=400, detail="Missing required fields")

    # Verify signature based on mode
    signature_valid = False

    if settings.paypal_mode == "demo_hmac":
        # Demo HMAC verification for offline development
        demo_signature = headers.get("x-demo-signature", "")
        signature_valid = verify_demo_hmac(
            payload=body, signature=demo_signature, secret=settings.demo_hmac_secret
        )
        logger.info("Using demo HMAC verification for PayPal webhook")
    else:
        # Real PayPal verification
        try:
            access_token = await get_paypal_access_token(
                settings.paypal_client_id,
                settings.paypal_client_secret,
                settings.paypal_mode,
            )
            signature_valid = await verify_paypal_webhook_signature(
                headers=headers,
                body=body,
                webhook_id=settings.paypal_webhook_id,
                access_token=access_token,
                mode=settings.paypal_mode,
            )
        except Exception as e:
            logger.error(f"PayPal verification error: {e}")
            signature_valid = False

    if not signature_valid:
        logger.warning(
            "Invalid PayPal signature",
            extra={"event_id": event.id, "mode": settings.paypal_mode},
        )
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Check idempotency
    idempotency_key = make_idempotency_key("paypal", event.id)
    is_first_attempt = await ensure_idempotency(db, idempotency_key)

    if not is_first_attempt:
        logger.info(f"Duplicate PayPal webhook ignored: {event.id}")
        return WebhookResponse(
            status="ok", message="duplicate ignored", event_id=event.id
        )

    try:
        # Store event
        payment_event = PaymentEvent(
            provider="paypal",
            event_id=event.id,
            event_type=event.event_type,
            payload_json=body.decode("utf-8"),
        )
        db.add(payment_event)
        await db.commit()

        logger.info(
            f"Successfully processed PayPal webhook: {event.id}",
            extra={
                "event_id": event.id,
                "event_type": event.event_type,
                "provider": "paypal",
            },
        )

        return WebhookResponse(status="ok", message="processed", event_id=event.id)

    except Exception as e:
        await db.rollback()
        logger.error(
            f"Failed to store PayPal webhook: {e}",
            extra={
                "event_id": event.id,
                "event_type": event.event_type,
                "error": str(e),
            },
        )
        # In production, this would go to DLQ
        raise HTTPException(status_code=500, detail="Processing failed") from e
