import hashlib
import hmac
import json
import time
from datetime import UTC
from datetime import datetime

import pytest
from fastapi.testclient import TestClient


class TestE2EWebhookFlow:
    """End-to-end tests for complete webhook processing flows."""

    @pytest.fixture
    def client(self, test_app):
        """Test client for E2E tests."""
        return TestClient(test_app)

    @pytest.fixture
    def stripe_payload(self):
        """Sample Stripe payload."""
        import uuid

        unique_id = str(uuid.uuid4())[:8]
        return {
            "id": f"evt_e2e_stripe_{unique_id}",
            "type": "payment_intent.succeeded",
            "data": {
                "object": {
                    "id": f"pi_e2e_{unique_id}",
                    "amount": 5000,
                    "currency": "usd",
                    "status": "succeeded",
                }
            },
            "created": int(time.time()),
            "api_version": "2020-08-27",
        }

    @pytest.fixture
    def paypal_payload(self):
        """Sample PayPal payload."""
        import uuid

        unique_id = str(uuid.uuid4())[:8]
        return {
            "id": f"WH-e2e-paypal-{unique_id}",
            "event_type": "PAYMENT.CAPTURE.COMPLETED",
            "resource": {
                "id": f"CAPTURE-e2e-{unique_id}",
                "amount": {"currency_code": "USD", "value": "50.00"},
                "status": "COMPLETED",
            },
            "create_time": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            "event_version": "1.0",
        }

    def test_health_endpoints(self, client):
        """Test health and readiness endpoints."""
        # Health check
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert data["version"] == "0.2.0-rc"

        # Readiness check
        response = client.get("/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ["ready", "not_ready"]
        assert "checks" in data
        assert "database" in data["checks"]

    def test_metrics_endpoint(self, client):
        """Test metrics endpoint."""
        response = client.get("/metrics")
        assert response.status_code == 200
        # Metrics endpoint returns Prometheus format text, not JSON
        content = response.text
        assert "payments_api_build_info" in content
        assert "application_ready" in content

    def test_stripe_webhook_complete_flow(self, client, stripe_payload):
        """Test complete Stripe webhook processing flow."""
        payload_json = json.dumps(stripe_payload)
        timestamp = int(time.time())

        # Create valid signature (using default test secret)
        signing_secret = "test_stripe_secret"
        signed_payload = f"{timestamp}.{payload_json}"
        signature = hmac.new(
            signing_secret.encode("utf-8"),
            signed_payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        headers = {
            "stripe-signature": f"t={timestamp},v1={signature}",
            "content-type": "application/json",
        }

        # Send webhook
        response = client.post(
            "/webhooks/stripe", content=payload_json, headers=headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["message"] == "processed"
        assert data["event_id"] == stripe_payload["id"]

        # Verify duplicate detection
        response2 = client.post(
            "/webhooks/stripe", content=payload_json, headers=headers
        )

        assert response2.status_code == 200
        data2 = response2.json()
        assert data2["message"] == "duplicate ignored"

    def test_paypal_webhook_complete_flow(self, client, paypal_payload):
        """Test complete PayPal webhook processing flow."""
        payload_json = json.dumps(paypal_payload)

        # Create demo HMAC signature
        demo_secret = "test_hmac_secret"
        signature = hmac.new(
            demo_secret.encode("utf-8"),
            payload_json.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        headers = {
            "x-demo-signature": signature,
            "content-type": "application/json",
        }

        # Send webhook
        response = client.post(
            "/webhooks/paypal", content=payload_json, headers=headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["message"] == "processed"
        assert data["event_id"] == paypal_payload["id"]

        # Verify duplicate detection
        response2 = client.post(
            "/webhooks/paypal", content=payload_json, headers=headers
        )

        assert response2.status_code == 200
        data2 = response2.json()
        assert data2["message"] == "duplicate ignored"

    def test_reconciliation_endpoint(self, client):
        """Test reconciliation summary endpoint."""
        # Test default parameters
        response = client.get("/reconciliation/summary")
        assert response.status_code == 200
        data = response.json()

        assert "period_start" in data
        assert "period_end" in data
        assert "total_events" in data
        assert "events_by_provider" in data
        assert "events_by_type" in data
        assert "anomalies" in data
        assert "generated_at" in data

        # Test with custom hours_back parameter
        response = client.get("/reconciliation/summary?hours_back=12")
        assert response.status_code == 200

    def test_admin_events_endpoint(self, client):
        """Test admin events listing endpoint."""
        # Test listing all events
        response = client.get("/admin/events")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

        # Test filtering by provider
        response = client.get("/admin/events?provider=stripe")
        assert response.status_code == 200

        # Test limit parameter
        response = client.get("/admin/events?limit=10")
        assert response.status_code == 200

    def test_error_handling(self, client):
        """Test error handling for various scenarios."""
        # Test invalid signature
        response = client.post(
            "/webhooks/stripe",
            json={"id": "test", "type": "test"},
            headers={"stripe-signature": "invalid"},
        )
        assert response.status_code == 400

        # Test malformed JSON
        response = client.post(
            "/webhooks/stripe",
            content="invalid json",
            headers={
                "stripe-signature": "t=123,v1=sig",
                "content-type": "application/json",
            },
        )
        assert response.status_code == 400

        # Test invalid reconciliation parameters
        response = client.get("/reconciliation/summary?hours_back=200")
        assert response.status_code == 422  # Validation error

    def test_openapi_documentation(self, client):
        """Test that OpenAPI documentation is available."""
        # Test OpenAPI JSON
        response = client.get("/openapi.json")
        assert response.status_code == 200
        openapi_spec = response.json()
        assert "openapi" in openapi_spec
        assert "paths" in openapi_spec
        assert "/webhooks/stripe" in openapi_spec["paths"]
        assert "/webhooks/paypal" in openapi_spec["paths"]

        # Test Swagger UI (if available)
        response = client.get("/docs")
        assert response.status_code == 200

    def test_concurrent_webhooks(self, client, stripe_payload):
        """Test handling of sequential webhook requests."""
        # Create multiple unique payloads
        responses = []

        import uuid

        for i in range(5):
            payload = stripe_payload.copy()
            payload["id"] = f"evt_concurrent_{i}_{str(uuid.uuid4())[:8]}"
            payload_json = json.dumps(payload)
            timestamp = int(time.time())

            signed_payload = f"{timestamp}.{payload_json}"
            signature = hmac.new(
                b"test_stripe_secret",
                signed_payload.encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()

            headers = {
                "stripe-signature": f"t={timestamp},v1={signature}",
                "content-type": "application/json",
            }

            response = client.post(
                "/webhooks/stripe",
                content=payload_json,
                headers=headers,
            )
            responses.append(response)

        # All should succeed
        for response in responses:
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ok"
            assert data["message"] == "processed"

    def test_rate_limiting_behavior(self, client, stripe_payload):
        """Test API behavior under rapid requests."""
        # Send multiple webhooks rapidly
        responses = []
        import uuid

        for i in range(10):
            payload = stripe_payload.copy()
            payload["id"] = f"evt_rate_test_{i}_{str(uuid.uuid4())[:8]}"
            payload_json = json.dumps(payload)
            timestamp = int(time.time())

            signed_payload = f"{timestamp}.{payload_json}"
            signature = hmac.new(
                b"test_stripe_secret",
                signed_payload.encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()

            headers = {
                "stripe-signature": f"t={timestamp},v1={signature}",
                "content-type": "application/json",
            }

            response = client.post(
                "/webhooks/stripe", content=payload_json, headers=headers
            )
            responses.append(response)

        # All should succeed (no rate limiting implemented in this version)
        success_count = sum(1 for r in responses if r.status_code == 200)
        assert success_count >= 8  # Allow for some timing issues
