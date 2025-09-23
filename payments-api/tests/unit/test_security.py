"""Tests for security utilities."""

from app.utils.security import is_sensitive_key
from app.utils.security import mask_card_number
from app.utils.security import mask_email
from app.utils.security import mask_pii_in_dict
from app.utils.security import mask_pii_in_text
from app.utils.security import mask_token
from app.utils.security import sanitize_log_data


class TestPIIMasking:
    """Test PII masking functions."""

    def test_mask_email(self):
        """Test email masking."""
        text = "Contact user@example.com for support"
        result = mask_email(text)
        assert result == "Contact ***EMAIL*** for support"

    def test_mask_email_multiple(self):
        """Test masking multiple emails."""
        text = "Send to alice@test.com and bob@example.org"
        result = mask_email(text)
        assert result == "Send to ***EMAIL*** and ***EMAIL***"

    def test_mask_token_generic(self):
        """Test generic token masking."""
        text = "API key: abcdef1234567890abcdef1234567890abcdef12"
        result = mask_token(text)
        assert result == "API key: ***TOKEN***"

    def test_mask_token_stripe(self):
        """Test Stripe token masking."""
        text = "Secret: sk_test_1234567890abcdef1234567890"
        result = mask_token(text)
        assert result == "Secret: ***TOKEN***"

    def test_mask_token_bearer(self):
        """Test Bearer token masking."""
        text = "Authorization: Bearer abc123def456"
        result = mask_token(text)
        assert result == "Authorization: ***TOKEN***"

    def test_mask_card_number_16_digit(self):
        """Test 16-digit card masking."""
        text = "Card: 4111-1111-1111-1111"
        result = mask_card_number(text)
        assert result == "Card: ***CARD***"

    def test_mask_card_number_no_separators(self):
        """Test card masking without separators."""
        text = "Card: 4111111111111111"
        result = mask_card_number(text)
        assert result == "Card: ***CARD***"

    def test_mask_card_number_amex(self):
        """Test Amex card masking."""
        text = "Amex: 3711 123456 12345"
        result = mask_card_number(text)
        assert result == "Amex: ***CARD***"

    def test_mask_pii_in_text_comprehensive(self):
        """Test comprehensive PII masking."""
        text = "User john@test.com has card 4111111111111111 and token sk_test_abc123"
        result = mask_pii_in_text(text)
        assert "***EMAIL***" in result
        assert "***CARD***" in result
        assert "***TOKEN***" in result
        assert "john@test.com" not in result
        assert "4111111111111111" not in result
        assert "sk_test_abc123" not in result

    def test_mask_pii_in_dict(self):
        """Test PII masking in dictionary."""
        data = {
            "email": "user@example.com",
            "description": "Card ending in 1111",
            "meta": {"token": "sk_test_secret123"},
        }
        result = mask_pii_in_dict(data)
        assert result["email"] == "***EMAIL***"
        assert result["meta"]["token"] == "***TOKEN***"

    def test_is_sensitive_key(self):
        """Test sensitive key detection."""
        assert is_sensitive_key("password")
        assert is_sensitive_key("stripe_signing_secret")
        assert is_sensitive_key("api_key")
        assert is_sensitive_key("CLIENT_SECRET")
        assert not is_sensitive_key("name")
        assert not is_sensitive_key("amount")

    def test_sanitize_log_data_dict(self):
        """Test log data sanitization for dict."""
        data = {
            "name": "John Doe",
            "password": "secret123",
            "stripe_signing_secret": "sk_test_abc",
            "nested": {"api_key": "sensitive_value", "public_info": "safe_data"},
        }
        result = sanitize_log_data(data)
        assert result["name"] == "John Doe"
        assert result["password"] == "***MASKED***"
        assert result["stripe_signing_secret"] == "***MASKED***"
        assert result["nested"]["api_key"] == "***MASKED***"
        assert result["nested"]["public_info"] == "safe_data"

    def test_sanitize_log_data_string(self):
        """Test log data sanitization for string."""
        text = "User email@test.com has token sk_test_123"
        result = sanitize_log_data(text)
        assert "***EMAIL***" in result
        assert "***TOKEN***" in result

    def test_sanitize_log_data_list(self):
        """Test log data sanitization for list."""
        data = ["email@test.com", "safe_text", "sk_test_token123"]
        result = sanitize_log_data(data)
        assert result[0] == "***EMAIL***"
        assert result[1] == "safe_text"
        assert result[2] == "***TOKEN***"

    def test_mask_pii_non_string_input(self):
        """Test PII masking with non-string input."""
        assert mask_pii_in_text(123) == "123"
        assert mask_pii_in_text(None) == "None"
        assert mask_pii_in_text([]) == "[]"
