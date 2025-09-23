"""Integration tests for security features."""

import json


class TestRequestSizeLimiting:
    """Test request body size limiting."""

    def test_request_under_limit(self, client):
        """Test request under size limit passes through."""
        payload = {"id": "test_123", "type": "test", "data": {"test": "data"}}
        response = client.post(
            "/webhooks/stripe",
            json=payload,
            headers={"stripe-signature": "t=123,v1=invalid"},
        )
        # Should get 400 for invalid signature, not 413 for size
        assert response.status_code == 400
        assert "signature" in response.json()["detail"]

    def test_request_over_limit_content_length(self, client, monkeypatch):
        """Test request over size limit with content-length header."""
        # Set a small limit for testing
        monkeypatch.setenv("MAX_REQUEST_SIZE", "100")

        # Create a large payload
        large_payload = {"data": "x" * 200}

        response = client.post(
            "/webhooks/stripe",
            json=large_payload,
            headers={
                "content-length": str(len(json.dumps(large_payload))),
                "stripe-signature": "t=123,v1=valid",
            },
        )

        assert response.status_code == 413
        assert "Request body too large" in response.json()["detail"]

    def test_request_invalid_content_length(self, client):
        """Test request with invalid content-length header."""
        payload = {"id": "test_123", "type": "test", "data": {"test": "data"}}
        response = client.post(
            "/webhooks/stripe",
            json=payload,
            headers={
                "content-length": "invalid",
                "stripe-signature": "t=123,v1=invalid",
            },
        )
        # Should pass through middleware and get signature error
        assert response.status_code == 400
        assert "signature" in response.json()["detail"]

    def test_request_no_content_length(self, client):
        """Test request without content-length header."""
        payload = {"id": "test_123", "type": "test", "data": {"test": "data"}}
        response = client.post(
            "/webhooks/stripe",
            json=payload,
            headers={"stripe-signature": "t=123,v1=invalid"},
        )
        # Should pass through middleware and get signature error
        assert response.status_code == 400
        assert "signature" in response.json()["detail"]


class TestTimestampTolerance:
    """Test Stripe timestamp tolerance configuration."""

    def test_stripe_timestamp_within_tolerance(self, client, monkeypatch):
        """Test webhook with timestamp within tolerance."""
        import hashlib
        import hmac
        import time

        # Use current timestamp (should be within default 5 minute tolerance)
        timestamp = int(time.time())
        payload = {
            "id": "evt_test",
            "type": "test",
            "data": {},
            "created": int(time.time()),
        }
        payload_json = json.dumps(payload)

        signed_payload = f"{timestamp}.{payload_json}"
        signature = hmac.new(
            b"test_stripe_secret", signed_payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        response = client.post(
            "/webhooks/stripe",
            content=payload_json,
            headers={
                "stripe-signature": f"t={timestamp},v1={signature}",
                "content-type": "application/json",
            },
        )

        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_stripe_timestamp_outside_tolerance(self, test_db):
        """Test webhook with timestamp outside tolerance."""
        import hashlib
        import hmac
        import time

        from fastapi.testclient import TestClient

        from app.config import Settings
        from app.db import get_db
        from app.main import create_app

        # Create settings with short tolerance
        settings = Settings(
            stripe_timestamp_tolerance=60,  # 1 minute
            stripe_signing_secret="test_stripe_secret",
            demo_hmac_secret="test_hmac_secret",
        )

        # Create test app with custom settings
        app = create_app(settings)

        # Override database dependency
        async def override_get_db():
            yield test_db

        app.dependency_overrides[get_db] = override_get_db

        # Create test client
        with TestClient(app) as client:
            # Use old timestamp (2 minutes ago)
            timestamp = int(time.time()) - 120
            payload = {
                "id": "evt_old",
                "type": "test",
                "data": {},
                "created": int(time.time()),
            }
            payload_json = json.dumps(payload)

            signed_payload = f"{timestamp}.{payload_json}"
            signature = hmac.new(
                b"test_stripe_secret", signed_payload.encode("utf-8"), hashlib.sha256
            ).hexdigest()

            response = client.post(
                "/webhooks/stripe",
                content=payload_json,
                headers={
                    "stripe-signature": f"t={timestamp},v1={signature}",
                    "content-type": "application/json",
                },
            )

            assert response.status_code == 400
            assert "Invalid signature" in response.json()["detail"]

    def test_stripe_timestamp_future_outside_tolerance(self, test_db):
        """Test webhook with future timestamp outside tolerance."""
        import hashlib
        import hmac
        import time

        from fastapi.testclient import TestClient

        from app.config import Settings
        from app.db import get_db
        from app.main import create_app

        # Create settings with short tolerance
        settings = Settings(
            stripe_timestamp_tolerance=60,  # 1 minute
            stripe_signing_secret="test_stripe_secret",
            demo_hmac_secret="test_hmac_secret",
        )

        # Create test app with custom settings
        app = create_app(settings)

        # Override database dependency
        async def override_get_db():
            yield test_db

        app.dependency_overrides[get_db] = override_get_db

        # Create test client
        with TestClient(app) as client:
            # Use future timestamp (2 minutes from now)
            timestamp = int(time.time()) + 120
            payload = {
                "id": "evt_future",
                "type": "test",
                "data": {},
                "created": int(time.time()),
            }
            payload_json = json.dumps(payload)

            signed_payload = f"{timestamp}.{payload_json}"
            signature = hmac.new(
                b"test_stripe_secret", signed_payload.encode("utf-8"), hashlib.sha256
            ).hexdigest()

            response = client.post(
                "/webhooks/stripe",
                content=payload_json,
                headers={
                    "stripe-signature": f"t={timestamp},v1={signature}",
                    "content-type": "application/json",
                },
            )

            assert response.status_code == 400
            assert "Invalid signature" in response.json()["detail"]
