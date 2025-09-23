"""Advanced PayPal webhook tests for security scenarios."""

import hashlib
import hmac
import json
from unittest.mock import patch


class TestPayPalWebhookSecurity:
    """Test PayPal webhook security scenarios."""

    def test_paypal_demo_hmac_valid(self, client):
        """Test PayPal webhook with valid demo HMAC."""
        payload = {
            "id": "WH-demo-valid",
            "event_type": "PAYMENT.CAPTURE.COMPLETED",
            "resource": {"id": "CAPTURE-123"},
            "create_time": "2023-03-01T10:00:00Z",
        }
        payload_json = json.dumps(payload)

        # Create valid demo HMAC signature
        signature = hmac.new(
            b"test_hmac_secret", payload_json.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        response = client.post(
            "/webhooks/paypal",
            content=payload_json,
            headers={"x-demo-signature": signature, "content-type": "application/json"},
        )

        assert response.status_code == 200
        assert response.json()["status"] == "ok"
        assert response.json()["message"] == "processed"

    def test_paypal_demo_hmac_invalid(self, client):
        """Test PayPal webhook with invalid demo HMAC."""
        payload = {
            "id": "WH-demo-invalid",
            "event_type": "PAYMENT.CAPTURE.COMPLETED",
            "resource": {"id": "CAPTURE-456"},
            "create_time": "2023-03-01T10:00:00Z",
        }
        payload_json = json.dumps(payload)

        # Use wrong secret for signature
        signature = hmac.new(
            b"wrong_secret", payload_json.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        response = client.post(
            "/webhooks/paypal",
            content=payload_json,
            headers={"x-demo-signature": signature, "content-type": "application/json"},
        )

        assert response.status_code == 400
        assert "Invalid signature" in response.json()["detail"]

    def test_paypal_demo_hmac_missing_signature(self, client):
        """Test PayPal webhook missing demo signature header."""
        payload = {
            "id": "WH-demo-missing",
            "event_type": "PAYMENT.CAPTURE.COMPLETED",
            "resource": {"id": "CAPTURE-789"},
            "create_time": "2023-03-01T10:00:00Z",
        }

        response = client.post(
            "/webhooks/paypal",
            json=payload,
            headers={"content-type": "application/json"},
        )

        assert response.status_code == 400
        assert "Invalid signature" in response.json()["detail"]

    def test_paypal_demo_hmac_empty_signature(self, client):
        """Test PayPal webhook with empty demo signature."""
        payload = {
            "id": "WH-demo-empty",
            "event_type": "PAYMENT.CAPTURE.COMPLETED",
            "resource": {"id": "CAPTURE-empty"},
            "create_time": "2023-03-01T10:00:00Z",
        }

        response = client.post(
            "/webhooks/paypal",
            json=payload,
            headers={"x-demo-signature": "", "content-type": "application/json"},
        )

        assert response.status_code == 400
        assert "Invalid signature" in response.json()["detail"]

    @patch("app.webhooks.paypal.get_paypal_access_token")
    @patch("app.webhooks.paypal.verify_paypal_webhook_signature")
    def test_paypal_production_verification_success(
        self, mock_verify, mock_token, test_db
    ):
        """Test PayPal production verification returning SUCCESS."""
        from fastapi.testclient import TestClient

        from app.config import Settings
        from app.db import get_db
        from app.main import create_app

        # Create settings for sandbox mode
        settings = Settings(
            paypal_mode="sandbox",
            paypal_client_id="test_client_id",
            paypal_client_secret="test_client_secret",
            paypal_webhook_id="test_webhook_id",
            stripe_signing_secret="test_stripe_secret",
            demo_hmac_secret="test_hmac_secret",
        )

        # Create test app with sandbox settings
        app = create_app(settings)

        # Override database dependency
        async def override_get_db():
            yield test_db

        app.dependency_overrides[get_db] = override_get_db

        # Create test client
        with TestClient(app) as client:
            mock_token.return_value = "access_token_123"
            mock_verify.return_value = True

            payload = {
                "id": "WH-prod-success",
                "event_type": "PAYMENT.CAPTURE.COMPLETED",
                "resource": {"id": "CAPTURE-prod"},
                "create_time": "2023-03-01T10:00:00Z",
            }

            # Include required PayPal headers
            headers = {
                "content-type": "application/json",
                "PAYPAL-TRANSMISSION-ID": "12345",
                "PAYPAL-TRANSMISSION-TIME": "2023-03-01T10:00:00Z",
                "PAYPAL-CERT-URL": "https://api.paypal.com/cert",
                "PAYPAL-AUTH-ALGO": "SHA256withRSA",
                "PAYPAL-TRANSMISSION-SIG": "signature123",
            }

            response = client.post("/webhooks/paypal", json=payload, headers=headers)

            assert response.status_code == 200
            assert response.json()["status"] == "ok"
            mock_token.assert_called_once()
            mock_verify.assert_called_once()

    @patch("app.webhooks.paypal.get_paypal_access_token")
    @patch("app.webhooks.paypal.verify_paypal_webhook_signature")
    def test_paypal_production_verification_failure(
        self, mock_verify, mock_token, client, monkeypatch
    ):
        """Test PayPal production verification returning FAILURE."""
        # Switch to production mode
        monkeypatch.setenv("PAYPAL_MODE", "sandbox")
        monkeypatch.setenv("PAYPAL_CLIENT_ID", "test_client_id")
        monkeypatch.setenv("PAYPAL_CLIENT_SECRET", "test_client_secret")
        monkeypatch.setenv("PAYPAL_WEBHOOK_ID", "test_webhook_id")

        mock_token.return_value = "access_token_123"
        mock_verify.return_value = False

        payload = {
            "id": "WH-prod-failure",
            "event_type": "PAYMENT.CAPTURE.COMPLETED",
            "resource": {"id": "CAPTURE-fail"},
            "create_time": "2023-03-01T10:00:00Z",
        }

        headers = {
            "content-type": "application/json",
            "PAYPAL-TRANSMISSION-ID": "12345",
            "PAYPAL-TRANSMISSION-TIME": "2023-03-01T10:00:00Z",
            "PAYPAL-CERT-URL": "https://api.paypal.com/cert",
            "PAYPAL-AUTH-ALGO": "SHA256withRSA",
            "PAYPAL-TRANSMISSION-SIG": "bad_signature",
        }

        response = client.post("/webhooks/paypal", json=payload, headers=headers)

        assert response.status_code == 400
        assert "Invalid signature" in response.json()["detail"]

    @patch("app.webhooks.paypal.get_paypal_access_token")
    def test_paypal_production_token_failure(self, mock_token, client, monkeypatch):
        """Test PayPal production mode with token acquisition failure."""
        # Switch to production mode
        monkeypatch.setenv("PAYPAL_MODE", "sandbox")
        monkeypatch.setenv("PAYPAL_CLIENT_ID", "test_client_id")
        monkeypatch.setenv("PAYPAL_CLIENT_SECRET", "test_client_secret")

        # Mock token failure
        from fastapi import HTTPException

        mock_token.side_effect = HTTPException(
            status_code=500, detail="Failed to get PayPal access token"
        )

        payload = {
            "id": "WH-token-fail",
            "event_type": "PAYMENT.CAPTURE.COMPLETED",
            "resource": {"id": "CAPTURE-token"},
            "create_time": "2023-03-01T10:00:00Z",
        }

        headers = {
            "content-type": "application/json",
            "PAYPAL-TRANSMISSION-ID": "12345",
            "PAYPAL-TRANSMISSION-TIME": "2023-03-01T10:00:00Z",
            "PAYPAL-CERT-URL": "https://api.paypal.com/cert",
            "PAYPAL-AUTH-ALGO": "SHA256withRSA",
            "PAYPAL-TRANSMISSION-SIG": "signature123",
        }

        response = client.post("/webhooks/paypal", json=payload, headers=headers)

        assert response.status_code == 400
        assert "Invalid signature" in response.json()["detail"]

    def test_paypal_missing_required_headers_production(self, client, monkeypatch):
        """Test PayPal production mode missing required headers."""
        # Switch to production mode
        monkeypatch.setenv("PAYPAL_MODE", "sandbox")
        monkeypatch.setenv("PAYPAL_CLIENT_ID", "test_client_id")
        monkeypatch.setenv("PAYPAL_CLIENT_SECRET", "test_client_secret")

        payload = {
            "id": "WH-missing-headers",
            "event_type": "PAYMENT.CAPTURE.COMPLETED",
            "resource": {"id": "CAPTURE-headers"},
            "create_time": "2023-03-01T10:00:00Z",
        }

        # Missing required PayPal headers
        response = client.post(
            "/webhooks/paypal",
            json=payload,
            headers={"content-type": "application/json"},
        )

        assert response.status_code == 400
        assert "Invalid signature" in response.json()["detail"]


class TestPayPalWebhookValidation:
    """Test PayPal webhook validation scenarios."""

    def test_paypal_missing_id_field(self, client):
        """Test PayPal webhook missing required id field."""
        payload = {
            "event_type": "PAYMENT.CAPTURE.COMPLETED",  # Missing id
            "resource": {"id": "CAPTURE-123"},
            "create_time": "2023-03-01T10:00:00Z",
        }
        payload_json = json.dumps(payload)

        signature = hmac.new(
            b"test_hmac_secret", payload_json.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        response = client.post(
            "/webhooks/paypal",
            content=payload_json,
            headers={"x-demo-signature": signature, "content-type": "application/json"},
        )

        assert response.status_code == 400
        assert "Invalid JSON payload" in response.json()["detail"]

    def test_paypal_missing_event_type_field(self, client):
        """Test PayPal webhook missing required event_type field."""
        payload = {
            "id": "WH-missing-type",  # Missing event_type
            "resource": {"id": "CAPTURE-123"},
            "create_time": "2023-03-01T10:00:00Z",
        }
        payload_json = json.dumps(payload)

        signature = hmac.new(
            b"test_hmac_secret", payload_json.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        response = client.post(
            "/webhooks/paypal",
            content=payload_json,
            headers={"x-demo-signature": signature, "content-type": "application/json"},
        )

        assert response.status_code == 400
        assert "Invalid JSON payload" in response.json()["detail"]

    def test_paypal_malformed_json(self, client):
        """Test PayPal webhook with malformed JSON."""
        malformed_json = '{"id": "test", "event_type": invalid}'

        signature = hmac.new(
            b"test_hmac_secret", malformed_json.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        response = client.post(
            "/webhooks/paypal",
            content=malformed_json,
            headers={"x-demo-signature": signature, "content-type": "application/json"},
        )

        assert response.status_code == 400
        assert "Invalid JSON payload" in response.json()["detail"]
