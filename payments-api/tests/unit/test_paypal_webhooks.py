import json
from unittest.mock import AsyncMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest
from fastapi import HTTPException

from app.models import PaymentEvent
from app.webhooks.paypal import get_paypal_access_token
from app.webhooks.paypal import process_paypal_webhook
from app.webhooks.paypal import verify_paypal_webhook_signature


class TestGetPayPalAccessToken:
    """Test cases for get_paypal_access_token function."""

    @pytest.mark.asyncio
    async def test_get_access_token_sandbox_success(self):
        """Test successful access token retrieval for sandbox."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "test_token_123"}

        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post.return_value = (
                mock_response
            )

            token = await get_paypal_access_token(
                client_id="test_client", client_secret="test_secret", mode="sandbox"
            )

            assert token == "test_token_123"

            # Verify correct URL was used
            call_args = mock_client.return_value.__aenter__.return_value.post.call_args
            assert "api.sandbox.paypal.com" in call_args[0][0]

    @pytest.mark.asyncio
    async def test_get_access_token_live_success(self):
        """Test successful access token retrieval for live."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "live_token_456"}

        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post.return_value = (
                mock_response
            )

            token = await get_paypal_access_token(
                client_id="live_client", client_secret="live_secret", mode="live"
            )

            assert token == "live_token_456"

            # Verify correct URL was used
            call_args = mock_client.return_value.__aenter__.return_value.post.call_args
            assert "api.paypal.com" in call_args[0][0]

    @pytest.mark.asyncio
    async def test_get_access_token_failure(self):
        """Test access token retrieval failure."""
        mock_response = Mock()
        mock_response.status_code = 401

        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post.return_value = (
                mock_response
            )

            with pytest.raises(HTTPException) as exc_info:
                await get_paypal_access_token(
                    client_id="invalid_client",
                    client_secret="invalid_secret",
                    mode="sandbox",
                )

            assert exc_info.value.status_code == 500
            assert "Failed to get PayPal access token" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_get_access_token_request_parameters(self):
        """Test that request parameters are correct."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "test_token"}

        with patch("httpx.AsyncClient") as mock_client:
            mock_post = mock_client.return_value.__aenter__.return_value.post
            mock_post.return_value = mock_response

            await get_paypal_access_token(
                client_id="test_client", client_secret="test_secret", mode="sandbox"
            )

            # Verify request parameters
            call_args = mock_post.call_args
            assert call_args[1]["headers"]["Accept"] == "application/json"
            assert call_args[1]["headers"]["Accept-Language"] == "en_US"
            assert call_args[1]["auth"] == ("test_client", "test_secret")
            assert call_args[1]["data"] == "grant_type=client_credentials"


class TestVerifyPayPalWebhookSignature:
    """Test cases for verify_paypal_webhook_signature function."""

    @pytest.fixture
    def valid_headers(self):
        """Sample valid PayPal headers."""
        return {
            "PAYPAL-TRANSMISSION-ID": "test_transmission_id",
            "PAYPAL-TRANSMISSION-TIME": "2023-01-01T00:00:00Z",
            "PAYPAL-CERT-URL": "https://api.paypal.com/cert",
            "PAYPAL-AUTH-ALGO": "SHA256withRSA",
            "PAYPAL-TRANSMISSION-SIG": "test_signature",
        }

    @pytest.fixture
    def sample_body(self):
        """Sample webhook body."""
        return b'{"id": "test_event", "event_type": "PAYMENT.CAPTURE.COMPLETED", "create_time": "2023-01-01T00:00:00Z", "resource": {}}'

    @pytest.mark.asyncio
    async def test_verify_signature_missing_headers(self, sample_body):
        """Test verification with missing required headers."""
        incomplete_headers = {
            "PAYPAL-TRANSMISSION-ID": "test_id",
            # Missing other required headers
        }

        result = await verify_paypal_webhook_signature(
            headers=incomplete_headers,
            body=sample_body,
            webhook_id="test_webhook_id",
            access_token="test_token",
            mode="sandbox",
        )

        assert result is False

    @pytest.mark.asyncio
    async def test_verify_signature_success(self, valid_headers, sample_body):
        """Test successful signature verification."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"verification_status": "SUCCESS"}

        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post.return_value = (
                mock_response
            )

            result = await verify_paypal_webhook_signature(
                headers=valid_headers,
                body=sample_body,
                webhook_id="test_webhook_id",
                access_token="test_token",
                mode="sandbox",
            )

            assert result is True

            # Verify correct API endpoint was called
            call_args = mock_client.return_value.__aenter__.return_value.post.call_args
            assert "api.sandbox.paypal.com" in call_args[0][0]
            assert "verify-webhook-signature" in call_args[0][0]

    @pytest.mark.asyncio
    async def test_verify_signature_failure_status(self, valid_headers, sample_body):
        """Test signature verification with failure status."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"verification_status": "FAILURE"}

        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post.return_value = (
                mock_response
            )

            result = await verify_paypal_webhook_signature(
                headers=valid_headers,
                body=sample_body,
                webhook_id="test_webhook_id",
                access_token="test_token",
                mode="live",  # Test live mode URL
            )

            assert result is False

            # Verify live API endpoint was used
            call_args = mock_client.return_value.__aenter__.return_value.post.call_args
            assert "api.paypal.com" in call_args[0][0]

    @pytest.mark.asyncio
    async def test_verify_signature_api_error(self, valid_headers, sample_body):
        """Test signature verification with API error."""
        mock_response = Mock()
        mock_response.status_code = 500

        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post.return_value = (
                mock_response
            )

            result = await verify_paypal_webhook_signature(
                headers=valid_headers,
                body=sample_body,
                webhook_id="test_webhook_id",
                access_token="test_token",
                mode="sandbox",
            )

            assert result is False

    @pytest.mark.asyncio
    async def test_verify_signature_exception(self, valid_headers, sample_body):
        """Test signature verification with exception."""
        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post.side_effect = (
                Exception("Network error")
            )

            result = await verify_paypal_webhook_signature(
                headers=valid_headers,
                body=sample_body,
                webhook_id="test_webhook_id",
                access_token="test_token",
                mode="sandbox",
            )

            assert result is False

    @pytest.mark.asyncio
    async def test_verify_signature_request_payload(self, valid_headers, sample_body):
        """Test that verification request payload is correct."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"verification_status": "SUCCESS"}

        with patch("httpx.AsyncClient") as mock_client:
            mock_post = mock_client.return_value.__aenter__.return_value.post
            mock_post.return_value = mock_response

            await verify_paypal_webhook_signature(
                headers=valid_headers,
                body=sample_body,
                webhook_id="test_webhook_id",
                access_token="test_token",
                mode="sandbox",
            )

            # Verify request payload structure
            call_args = mock_post.call_args
            verification_data = call_args[1]["json"]

            assert (
                verification_data["transmission_id"]
                == valid_headers["PAYPAL-TRANSMISSION-ID"]
            )
            assert verification_data["webhook_id"] == "test_webhook_id"
            assert verification_data["webhook_event"] == json.loads(
                sample_body.decode("utf-8")
            )

            # Verify headers
            headers = call_args[1]["headers"]
            assert headers["Authorization"] == "Bearer test_token"
            assert headers["Content-Type"] == "application/json"


class TestProcessPayPalWebhook:
    """Test cases for process_paypal_webhook function."""

    @pytest.fixture
    def mock_request(self):
        """Create a mock FastAPI request."""
        request = Mock()
        request.body = AsyncMock()
        request.headers = {}
        return request

    @pytest.fixture
    def mock_db(self):
        """Create a mock database session."""
        db = AsyncMock()
        db.add = Mock()
        db.commit = AsyncMock()
        db.rollback = AsyncMock()
        return db

    @pytest.fixture
    def mock_settings(self):
        """Create mock settings."""
        settings = Mock()
        settings.paypal_mode = "demo_hmac"
        settings.demo_hmac_secret = "test_secret"
        settings.paypal_client_id = "test_client"
        settings.paypal_client_secret = "test_secret"
        settings.paypal_webhook_id = "test_webhook_id"
        return settings

    @pytest.fixture
    def valid_payload(self):
        """Valid PayPal webhook payload."""
        return {
            "id": "WH-test123",
            "event_type": "PAYMENT.CAPTURE.COMPLETED",
            "resource": {"id": "payment_123"},
            "create_time": "2023-01-01T00:00:00Z",
        }

    @pytest.mark.asyncio
    async def test_process_webhook_invalid_json(
        self, mock_request, mock_db, mock_settings
    ):
        """Test processing webhook with invalid JSON."""
        mock_request.body.return_value = b"invalid json"

        with pytest.raises(HTTPException) as exc_info:
            await process_paypal_webhook(mock_request, mock_db, mock_settings)

        assert exc_info.value.status_code == 400
        assert "Invalid JSON payload" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_process_webhook_missing_fields(
        self, mock_request, mock_db, mock_settings
    ):
        """Test processing webhook with missing required fields."""
        invalid_payload = {
            "event_type": "PAYMENT.CAPTURE.COMPLETED",
            "create_time": "2023-01-01T00:00:00Z",
            "resource": {},
        }  # Missing id
        mock_request.body.return_value = json.dumps(invalid_payload).encode()

        with pytest.raises(HTTPException) as exc_info:
            await process_paypal_webhook(mock_request, mock_db, mock_settings)

        assert exc_info.value.status_code == 400
        assert "Invalid JSON payload" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_process_webhook_demo_hmac_invalid_signature(
        self, mock_request, mock_db, mock_settings, valid_payload
    ):
        """Test processing webhook with invalid demo HMAC signature."""
        mock_request.body.return_value = json.dumps(valid_payload).encode()
        mock_request.headers = {"x-demo-signature": "invalid_signature"}

        with patch("app.webhooks.paypal.verify_demo_hmac", return_value=False):
            with pytest.raises(HTTPException) as exc_info:
                await process_paypal_webhook(mock_request, mock_db, mock_settings)

            assert exc_info.value.status_code == 400
            assert "Invalid signature" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_process_webhook_demo_hmac_success(
        self, mock_request, mock_db, mock_settings, valid_payload
    ):
        """Test successful processing with demo HMAC."""
        mock_request.body.return_value = json.dumps(valid_payload).encode()
        mock_request.headers = {"x-demo-signature": "valid_signature"}

        with patch("app.webhooks.paypal.verify_demo_hmac", return_value=True):
            with patch("app.webhooks.paypal.ensure_idempotency", return_value=True):
                with patch(
                    "app.webhooks.paypal.make_idempotency_key", return_value="key"
                ):
                    response = await process_paypal_webhook(
                        mock_request, mock_db, mock_settings
                    )

                    assert response.status == "ok"
                    assert response.event_id == "WH-test123"
                    mock_db.add.assert_called_once()
                    mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_process_webhook_duplicate(
        self, mock_request, mock_db, mock_settings, valid_payload
    ):
        """Test processing duplicate webhook."""
        mock_request.body.return_value = json.dumps(valid_payload).encode()
        mock_request.headers = {"x-demo-signature": "valid_signature"}

        with patch("app.webhooks.paypal.verify_demo_hmac", return_value=True):
            with patch(
                "app.webhooks.paypal.ensure_idempotency", return_value=False
            ):  # Duplicate
                with patch(
                    "app.webhooks.paypal.make_idempotency_key", return_value="key"
                ):
                    response = await process_paypal_webhook(
                        mock_request, mock_db, mock_settings
                    )

                    assert response.status == "ok"
                    assert response.message == "duplicate ignored"
                    mock_db.add.assert_not_called()

    @pytest.mark.asyncio
    async def test_process_webhook_real_paypal_success(
        self, mock_request, mock_db, valid_payload
    ):
        """Test successful processing with real PayPal verification."""
        # Set up real PayPal mode
        settings = Mock()
        settings.paypal_mode = "sandbox"
        settings.paypal_client_id = "test_client"
        settings.paypal_client_secret = "test_secret"
        settings.paypal_webhook_id = "test_webhook_id"

        mock_request.body.return_value = json.dumps(valid_payload).encode()
        mock_request.headers = {"PAYPAL-TRANSMISSION-ID": "test_id"}

        with patch(
            "app.webhooks.paypal.get_paypal_access_token", return_value="access_token"
        ):
            with patch(
                "app.webhooks.paypal.verify_paypal_webhook_signature", return_value=True
            ):
                with patch("app.webhooks.paypal.ensure_idempotency", return_value=True):
                    with patch(
                        "app.webhooks.paypal.make_idempotency_key", return_value="key"
                    ):
                        response = await process_paypal_webhook(
                            mock_request, mock_db, settings
                        )

                        assert response.status == "ok"
                        assert response.event_id == "WH-test123"

    @pytest.mark.asyncio
    async def test_process_webhook_real_paypal_verification_error(
        self, mock_request, mock_db, valid_payload
    ):
        """Test processing with PayPal verification error."""
        # Set up real PayPal mode
        settings = Mock()
        settings.paypal_mode = "sandbox"
        settings.paypal_client_id = "test_client"
        settings.paypal_client_secret = "test_secret"
        settings.paypal_webhook_id = "test_webhook_id"

        mock_request.body.return_value = json.dumps(valid_payload).encode()
        mock_request.headers = {"PAYPAL-TRANSMISSION-ID": "test_id"}

        with patch(
            "app.webhooks.paypal.get_paypal_access_token",
            side_effect=Exception("Auth error"),
        ):
            with pytest.raises(HTTPException) as exc_info:
                await process_paypal_webhook(mock_request, mock_db, settings)

            assert exc_info.value.status_code == 400
            assert "Invalid signature" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_process_webhook_database_error(
        self, mock_request, mock_db, mock_settings, valid_payload
    ):
        """Test processing webhook with database error."""
        mock_request.body.return_value = json.dumps(valid_payload).encode()
        mock_request.headers = {"x-demo-signature": "valid_signature"}

        # Mock database to raise exception on commit
        mock_db.commit.side_effect = Exception("Database error")

        with patch("app.webhooks.paypal.verify_demo_hmac", return_value=True):
            with patch("app.webhooks.paypal.ensure_idempotency", return_value=True):
                with patch(
                    "app.webhooks.paypal.make_idempotency_key", return_value="key"
                ):
                    with pytest.raises(HTTPException) as exc_info:
                        await process_paypal_webhook(
                            mock_request, mock_db, mock_settings
                        )

                    assert exc_info.value.status_code == 500
                    assert "Processing failed" in str(exc_info.value.detail)
                    mock_db.rollback.assert_called_once()

    @pytest.mark.asyncio
    async def test_process_webhook_payment_event_creation(
        self, mock_request, mock_db, mock_settings, valid_payload
    ):
        """Test that PaymentEvent is created correctly."""
        mock_request.body.return_value = json.dumps(valid_payload).encode()
        mock_request.headers = {"x-demo-signature": "valid_signature"}

        with patch("app.webhooks.paypal.verify_demo_hmac", return_value=True):
            with patch("app.webhooks.paypal.ensure_idempotency", return_value=True):
                with patch(
                    "app.webhooks.paypal.make_idempotency_key", return_value="key"
                ):
                    await process_paypal_webhook(mock_request, mock_db, mock_settings)

                    # Verify PaymentEvent was created with correct data
                    mock_db.add.assert_called_once()
                    payment_event = mock_db.add.call_args[0][0]
                    assert isinstance(payment_event, PaymentEvent)
                    assert payment_event.provider == "paypal"
                    assert payment_event.event_id == "WH-test123"
                    assert payment_event.event_type == "PAYMENT.CAPTURE.COMPLETED"
                    assert payment_event.payload_json == json.dumps(valid_payload)
