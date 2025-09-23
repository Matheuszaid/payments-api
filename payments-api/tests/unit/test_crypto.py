import hashlib
import hmac
import time

from app.utils.crypto import constant_time_compare
from app.utils.crypto import parse_stripe_signature
from app.utils.crypto import verify_demo_hmac
from app.utils.crypto import verify_stripe_signature


class TestConstantTimeCompare:
    """Test constant-time string comparison."""

    def test_equal_strings(self):
        """Test comparison of equal strings."""
        assert constant_time_compare("hello", "hello") is True

    def test_different_strings(self):
        """Test comparison of different strings."""
        assert constant_time_compare("hello", "world") is False

    def test_different_lengths(self):
        """Test comparison of strings with different lengths."""
        assert constant_time_compare("hello", "hello world") is False

    def test_empty_strings(self):
        """Test comparison of empty strings."""
        assert constant_time_compare("", "") is True

    def test_one_empty_string(self):
        """Test comparison with one empty string."""
        assert constant_time_compare("hello", "") is False


class TestParseStripeSignature:
    """Test Stripe signature header parsing."""

    def test_valid_signature_header(self):
        """Test parsing valid signature header."""
        header = "t=1677649200,v1=signature123"
        result = parse_stripe_signature(header)
        assert result == (1677649200, "signature123")

    def test_multiple_signatures(self):
        """Test parsing header with multiple signatures (takes v1)."""
        header = "t=1677649200,v1=signature123,v1=signature456"
        result = parse_stripe_signature(header)
        assert result == (1677649200, "signature123")

    def test_missing_timestamp(self):
        """Test parsing header missing timestamp."""
        header = "v1=signature123"
        result = parse_stripe_signature(header)
        assert result is None

    def test_missing_signature(self):
        """Test parsing header missing signature."""
        header = "t=1677649200"
        result = parse_stripe_signature(header)
        assert result is None

    def test_invalid_timestamp(self):
        """Test parsing header with invalid timestamp."""
        header = "t=invalid,v1=signature123"
        result = parse_stripe_signature(header)
        assert result is None

    def test_empty_header(self):
        """Test parsing empty header."""
        result = parse_stripe_signature("")
        assert result is None

    def test_malformed_header(self):
        """Test parsing malformed header."""
        header = "invalid_format"
        result = parse_stripe_signature(header)
        assert result is None


class TestVerifyStripeSignature:
    """Test Stripe signature verification."""

    def test_valid_signature(self):
        """Test verification of valid signature."""
        payload = b'{"id":"evt_test","type":"test"}'
        secret = "test_secret"
        timestamp = int(time.time())

        # Create valid signature
        signed_payload = f"{timestamp}.{payload.decode('utf-8')}"
        signature = hmac.new(
            secret.encode("utf-8"), signed_payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        header = f"t={timestamp},v1={signature}"

        assert verify_stripe_signature(payload, header, secret) is True

    def test_invalid_signature(self):
        """Test verification of invalid signature."""
        payload = b'{"id":"evt_test","type":"test"}'
        secret = "test_secret"
        timestamp = int(time.time())

        header = f"t={timestamp},v1=invalid_signature"

        assert verify_stripe_signature(payload, header, secret) is False

    def test_expired_signature(self):
        """Test verification of expired signature."""
        payload = b'{"id":"evt_test","type":"test"}'
        secret = "test_secret"
        timestamp = int(time.time()) - 400  # 400 seconds ago (beyond tolerance)

        # Create valid signature but with old timestamp
        signed_payload = f"{timestamp}.{payload.decode('utf-8')}"
        signature = hmac.new(
            secret.encode("utf-8"), signed_payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        header = f"t={timestamp},v1={signature}"

        assert verify_stripe_signature(payload, header, secret) is False

    def test_empty_secret(self):
        """Test verification with empty secret."""
        payload = b'{"id":"evt_test","type":"test"}'
        timestamp = int(time.time())
        header = f"t={timestamp},v1=signature"

        assert verify_stripe_signature(payload, header, "") is False

    def test_malformed_header(self):
        """Test verification with malformed header."""
        payload = b'{"id":"evt_test","type":"test"}'
        secret = "test_secret"

        assert verify_stripe_signature(payload, "invalid", secret) is False


class TestVerifyDemoHmac:
    """Test demo HMAC verification."""

    def test_valid_hmac(self):
        """Test verification of valid HMAC."""
        payload = b'{"id":"evt_test","type":"test"}'
        secret = "test_secret"

        # Create valid HMAC
        signature = hmac.new(
            secret.encode("utf-8"), payload, hashlib.sha256
        ).hexdigest()

        assert verify_demo_hmac(payload, signature, secret) is True

    def test_invalid_hmac(self):
        """Test verification of invalid HMAC."""
        payload = b'{"id":"evt_test","type":"test"}'
        secret = "test_secret"

        assert verify_demo_hmac(payload, "invalid_signature", secret) is False

    def test_empty_secret(self):
        """Test verification with empty secret."""
        payload = b'{"id":"evt_test","type":"test"}'

        assert verify_demo_hmac(payload, "signature", "") is False

    def test_empty_signature(self):
        """Test verification with empty signature."""
        payload = b'{"id":"evt_test","type":"test"}'
        secret = "test_secret"

        assert verify_demo_hmac(payload, "", secret) is False

    def test_different_payload(self):
        """Test that different payload produces different signature."""
        payload1 = b'{"id":"evt_test_1","type":"test"}'
        payload2 = b'{"id":"evt_test_2","type":"test"}'
        secret = "test_secret"

        signature1 = hmac.new(
            secret.encode("utf-8"), payload1, hashlib.sha256
        ).hexdigest()

        assert verify_demo_hmac(payload2, signature1, secret) is False
