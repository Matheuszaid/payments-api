"""Advanced Stripe webhook tests for security scenarios."""

import hashlib
import hmac
import json
import time


class TestStripeWebhookSecurity:
    """Test Stripe webhook security scenarios."""

    def test_stripe_invalid_hmac_signature(self, client):
        """Test Stripe webhook with invalid HMAC."""
        payload = {
            "id": "evt_test",
            "type": "test",
            "data": {},
            "created": int(time.time()),
        }
        payload_json = json.dumps(payload)
        timestamp = int(time.time())

        # Use wrong secret for signature
        signed_payload = f"{timestamp}.{payload_json}"
        signature = hmac.new(
            b"wrong_secret", signed_payload.encode("utf-8"), hashlib.sha256
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

    def test_stripe_multiple_signature_headers(self, client):
        """Test Stripe webhook with multiple v1 signatures (should use first)."""
        payload = {
            "id": "evt_multi",
            "type": "test",
            "data": {},
            "created": int(time.time()),
        }
        payload_json = json.dumps(payload)
        timestamp = int(time.time())

        # Create correct signature
        signed_payload = f"{timestamp}.{payload_json}"
        correct_signature = hmac.new(
            b"test_stripe_secret", signed_payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        # Create wrong signature
        wrong_signature = hmac.new(
            b"wrong_secret", signed_payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        # First signature is correct, second is wrong - should succeed
        response = client.post(
            "/webhooks/stripe",
            content=payload_json,
            headers={
                "stripe-signature": f"t={timestamp},v1={correct_signature},v1={wrong_signature}",
                "content-type": "application/json",
            },
        )

        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_stripe_mutated_payload_after_signing(self, client):
        """Test Stripe webhook with payload mutated after signing."""
        original_payload = {
            "id": "evt_original",
            "type": "test",
            "data": {},
            "created": int(time.time()),
        }
        mutated_payload = {
            "id": "evt_mutated",
            "type": "test",
            "data": {},
            "created": int(time.time()),
        }

        timestamp = int(time.time())

        # Sign the original payload
        signed_payload = f"{timestamp}.{json.dumps(original_payload)}"
        signature = hmac.new(
            b"test_stripe_secret", signed_payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        # Send the mutated payload with original signature
        response = client.post(
            "/webhooks/stripe",
            content=json.dumps(mutated_payload),
            headers={
                "stripe-signature": f"t={timestamp},v1={signature}",
                "content-type": "application/json",
            },
        )

        assert response.status_code == 400
        assert "Invalid signature" in response.json()["detail"]

    def test_stripe_wrong_content_type(self, client):
        """Test Stripe webhook with wrong content-type."""
        payload = {
            "id": "evt_wrong_ct",
            "type": "test",
            "data": {},
            "created": int(time.time()),
        }
        payload_json = json.dumps(payload)
        timestamp = int(time.time())

        signed_payload = f"{timestamp}.{payload_json}"
        signature = hmac.new(
            b"test_stripe_secret", signed_payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        response = client.post(
            "/webhooks/stripe",
            content=payload_json,
            headers={
                "stripe-signature": f"t={timestamp},v1={signature}",
                "content-type": "text/plain",  # Wrong content type
            },
        )

        # Should still process (signature is valid)
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_stripe_malformed_signature_header(self, client):
        """Test various malformed signature headers."""
        payload = {
            "id": "evt_malformed",
            "type": "test",
            "data": {},
            "created": int(time.time()),
        }
        payload_json = json.dumps(payload)

        malformed_headers = [
            "",  # Empty
            "invalid",  # No format
            "t=abc,v1=def",  # Invalid timestamp
            "t=123",  # Missing signature
            "v1=abc123",  # Missing timestamp
            "t=123,v2=abc",  # Wrong version
            "t=123,v1=",  # Empty signature
        ]

        for bad_header in malformed_headers:
            response = client.post(
                "/webhooks/stripe",
                content=payload_json,
                headers={
                    "stripe-signature": bad_header,
                    "content-type": "application/json",
                },
            )

            assert response.status_code == 400
            assert "Invalid signature" in response.json()["detail"]

    def test_stripe_missing_signature_header(self, client):
        """Test Stripe webhook without signature header."""
        payload = {
            "id": "evt_no_sig",
            "type": "test",
            "data": {},
            "created": int(time.time()),
        }

        response = client.post(
            "/webhooks/stripe",
            json=payload,
            headers={"content-type": "application/json"},
        )

        assert response.status_code == 400
        assert "Invalid signature" in response.json()["detail"]

    def test_stripe_empty_secret(self, client, monkeypatch):
        """Test Stripe webhook with empty signing secret."""
        monkeypatch.setenv("STRIPE_SIGNING_SECRET", "")

        payload = {
            "id": "evt_empty_secret",
            "type": "test",
            "data": {},
            "created": int(time.time()),
        }
        payload_json = json.dumps(payload)
        timestamp = int(time.time())

        response = client.post(
            "/webhooks/stripe",
            content=payload_json,
            headers={
                "stripe-signature": f"t={timestamp},v1=anysignature",
                "content-type": "application/json",
            },
        )

        assert response.status_code == 400
        assert "Invalid signature" in response.json()["detail"]


class TestStripeWebhookValidation:
    """Test Stripe webhook validation scenarios."""

    def test_stripe_missing_id_field(self, client):
        """Test Stripe webhook missing required id field."""
        payload = {
            "type": "test",
            "data": {},
            "created": int(time.time()),
        }  # Missing id
        payload_json = json.dumps(payload)
        timestamp = int(time.time())

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
        assert "Invalid JSON payload" in response.json()["detail"]

    def test_stripe_missing_type_field(self, client):
        """Test Stripe webhook missing required type field."""
        payload = {
            "id": "evt_no_type",
            "data": {},
            "created": int(time.time()),
        }  # Missing type
        payload_json = json.dumps(payload)
        timestamp = int(time.time())

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
        assert "Invalid JSON payload" in response.json()["detail"]

    def test_stripe_malformed_json(self, client):
        """Test Stripe webhook with malformed JSON."""
        malformed_json = '{"id": "test", "type": "test", invalid}'
        timestamp = int(time.time())

        signed_payload = f"{timestamp}.{malformed_json}"
        signature = hmac.new(
            b"test_stripe_secret", signed_payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        response = client.post(
            "/webhooks/stripe",
            content=malformed_json,
            headers={
                "stripe-signature": f"t={timestamp},v1={signature}",
                "content-type": "application/json",
            },
        )

        assert response.status_code == 400
        assert "Invalid JSON payload" in response.json()["detail"]

    def test_stripe_non_json_payload(self, client):
        """Test Stripe webhook with non-JSON payload."""
        payload = "not json data"
        timestamp = int(time.time())

        signed_payload = f"{timestamp}.{payload}"
        signature = hmac.new(
            b"test_stripe_secret", signed_payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        response = client.post(
            "/webhooks/stripe",
            content=payload,
            headers={
                "stripe-signature": f"t={timestamp},v1={signature}",
                "content-type": "application/json",
            },
        )

        assert response.status_code == 400
        assert "Invalid JSON payload" in response.json()["detail"]
