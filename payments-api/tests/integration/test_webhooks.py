import hashlib
import hmac
import json
import time
from unittest.mock import AsyncMock
from unittest.mock import patch

from sqlalchemy import select

from app.models import IdempotencyKey
from app.models import PaymentEvent
from app.utils.idempotency import make_idempotency_key


class TestStripeWebhooks:
    """Integration tests for Stripe webhook processing."""

    def test_stripe_webhook_success(self, client, test_db, stripe_webhook_payload):
        """Test successful Stripe webhook processing."""
        payload_json = json.dumps(stripe_webhook_payload)
        timestamp = int(time.time())

        # Create valid signature
        signed_payload = f"{timestamp}.{payload_json}"
        signature = hmac.new(
            b"test_stripe_secret", signed_payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        headers = {
            "stripe-signature": f"t={timestamp},v1={signature}",
            "content-type": "application/json",
        }

        response = client.post(
            "/webhooks/stripe", content=payload_json, headers=headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["message"] == "processed"
        assert data["event_id"] == stripe_webhook_payload["id"]

    def test_stripe_webhook_invalid_signature(self, client, stripe_webhook_payload):
        """Test Stripe webhook with invalid signature."""
        payload_json = json.dumps(stripe_webhook_payload)
        timestamp = int(time.time())

        headers = {
            "stripe-signature": f"t={timestamp},v1=invalid_signature",
            "content-type": "application/json",
        }

        response = client.post(
            "/webhooks/stripe", content=payload_json, headers=headers
        )

        assert response.status_code == 400
        assert "Invalid signature" in response.json()["detail"]

    def test_stripe_webhook_duplicate(self, client, test_db, stripe_webhook_payload):
        """Test Stripe webhook duplicate detection."""
        payload_json = json.dumps(stripe_webhook_payload)
        timestamp = int(time.time())

        # Create valid signature
        signed_payload = f"{timestamp}.{payload_json}"
        signature = hmac.new(
            b"test_stripe_secret", signed_payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        headers = {
            "stripe-signature": f"t={timestamp},v1={signature}",
            "content-type": "application/json",
        }

        # First request
        response1 = client.post("/webhooks/stripe", data=payload_json, headers=headers)
        assert response1.status_code == 200
        assert response1.json()["message"] == "processed"

        # Second request (duplicate)
        response2 = client.post("/webhooks/stripe", data=payload_json, headers=headers)
        assert response2.status_code == 200
        assert response2.json()["message"] == "duplicate ignored"

    def test_stripe_webhook_malformed_json(self, client):
        """Test Stripe webhook with malformed JSON."""
        timestamp = int(time.time())
        payload = "invalid json"

        # Create signature for invalid payload
        signed_payload = f"{timestamp}.{payload}"
        signature = hmac.new(
            b"test_stripe_secret", signed_payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        headers = {
            "stripe-signature": f"t={timestamp},v1={signature}",
            "content-type": "application/json",
        }

        response = client.post("/webhooks/stripe", content=payload, headers=headers)

        assert response.status_code == 400
        assert "Invalid JSON payload" in response.json()["detail"]

    def test_stripe_webhook_missing_required_fields(self, client):
        """Test Stripe webhook with missing required fields."""
        payload = {"data": {"object": {}}}  # Missing id and type
        payload_json = json.dumps(payload)
        timestamp = int(time.time())

        signed_payload = f"{timestamp}.{payload_json}"
        signature = hmac.new(
            b"test_stripe_secret", signed_payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        headers = {
            "stripe-signature": f"t={timestamp},v1={signature}",
            "content-type": "application/json",
        }

        response = client.post(
            "/webhooks/stripe", content=payload_json, headers=headers
        )

        assert response.status_code == 400
        assert "Invalid JSON payload" in response.json()["detail"]


class TestPayPalWebhooks:
    """Integration tests for PayPal webhook processing."""

    def test_paypal_webhook_demo_hmac_success(
        self, client, test_db, paypal_webhook_payload
    ):
        """Test successful PayPal webhook with demo HMAC."""
        payload_json = json.dumps(paypal_webhook_payload)

        # Create demo HMAC signature
        signature = hmac.new(
            b"test_hmac_secret", payload_json.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        headers = {"x-demo-signature": signature, "content-type": "application/json"}

        response = client.post(
            "/webhooks/paypal", content=payload_json, headers=headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["message"] == "processed"
        assert data["event_id"] == paypal_webhook_payload["id"]

    def test_paypal_webhook_invalid_demo_hmac(self, client, paypal_webhook_payload):
        """Test PayPal webhook with invalid demo HMAC."""
        payload_json = json.dumps(paypal_webhook_payload)

        headers = {
            "x-demo-signature": "invalid_signature",
            "content-type": "application/json",
        }

        response = client.post(
            "/webhooks/paypal", content=payload_json, headers=headers
        )

        assert response.status_code == 400
        assert "Invalid signature" in response.json()["detail"]

    @patch("app.webhooks.paypal.get_paypal_access_token")
    @patch("app.webhooks.paypal.verify_paypal_webhook_signature")
    def test_paypal_webhook_real_verification_success(
        self,
        mock_verify,
        mock_token,
        client,
        test_db,
        paypal_webhook_payload,
        test_settings,
    ):
        """Test PayPal webhook with real verification (mocked)."""
        # Mock PayPal API responses
        mock_token.return_value = "test_access_token"
        mock_verify.return_value = True

        # Override settings for real mode
        test_settings.paypal_mode = "sandbox"
        with patch("app.config.get_settings", return_value=test_settings):
            payload_json = json.dumps(paypal_webhook_payload)

            headers = {
                "PAYPAL-TRANSMISSION-ID": "test-id",
                "PAYPAL-TRANSMISSION-TIME": "2023-03-01T10:00:00Z",
                "PAYPAL-CERT-URL": "https://api.sandbox.paypal.com/cert",
                "PAYPAL-AUTH-ALGO": "SHA256withRSA",
                "PAYPAL-TRANSMISSION-SIG": "test-sig",
                "content-type": "application/json",
            }

            response = client.post(
                "/webhooks/paypal", content=payload_json, headers=headers
            )

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ok"
            assert data["message"] == "processed"

    def test_paypal_webhook_duplicate(self, client, test_db, paypal_webhook_payload):
        """Test PayPal webhook duplicate detection."""
        payload_json = json.dumps(paypal_webhook_payload)

        # Create demo HMAC signature
        signature = hmac.new(
            b"test_hmac_secret", payload_json.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        headers = {"x-demo-signature": signature, "content-type": "application/json"}

        # First request
        response1 = client.post("/webhooks/paypal", data=payload_json, headers=headers)
        assert response1.status_code == 200
        assert response1.json()["message"] == "processed"

        # Second request (duplicate)
        response2 = client.post("/webhooks/paypal", data=payload_json, headers=headers)
        assert response2.status_code == 200
        assert response2.json()["message"] == "duplicate ignored"


async def test_webhook_database_persistence(
    test_db, test_settings, stripe_webhook_payload
):
    """Test that webhook events are correctly persisted to database."""
    from app.webhooks.stripe import process_stripe_webhook

    # Mock request object
    request = AsyncMock()
    request.body.return_value = json.dumps(stripe_webhook_payload).encode()

    timestamp = int(time.time())
    signed_payload = f"{timestamp}.{json.dumps(stripe_webhook_payload)}"
    signature = hmac.new(
        b"test_stripe_secret", signed_payload.encode("utf-8"), hashlib.sha256
    ).hexdigest()

    request.headers = {"stripe-signature": f"t={timestamp},v1={signature}"}

    # Process webhook
    await process_stripe_webhook(request, test_db, test_settings)

    # Verify database records
    event_query = select(PaymentEvent).where(
        PaymentEvent.event_id == stripe_webhook_payload["id"]
    )
    result = await test_db.execute(event_query)
    event = result.scalar_one_or_none()

    assert event is not None
    assert event.provider == "stripe"
    assert event.event_id == stripe_webhook_payload["id"]
    assert event.event_type == stripe_webhook_payload["type"]

    # Verify idempotency key
    key = make_idempotency_key("stripe", stripe_webhook_payload["id"])
    key_query = select(IdempotencyKey).where(IdempotencyKey.key == key)
    result = await test_db.execute(key_query)
    idempotency_record = result.scalar_one_or_none()

    assert idempotency_record is not None
    assert idempotency_record.key == key
