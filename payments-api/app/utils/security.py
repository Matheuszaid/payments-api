"""Security utilities for PII masking and sensitive data handling."""

import re
from typing import Any


def mask_email(text: str) -> str:
    """Mask email addresses in text."""
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    return re.sub(email_pattern, "***EMAIL***", text)


def mask_token(text: str) -> str:
    """Mask tokens and API keys in text."""
    # Common token patterns
    patterns = [
        r"\bsk_[a-zA-Z0-9_]{8,}\b",  # Stripe secret keys
        r"\bpk_[a-zA-Z0-9_]{8,}\b",  # Stripe public keys
        r"\btk_[a-zA-Z0-9_]{8,}\b",  # Generic tokens
        r"\bbearer\s+[a-zA-Z0-9_.-]+\b",  # Bearer tokens
        r"\b[a-zA-Z0-9]{40,}\b",  # Generic long tokens (40+ chars)
    ]

    result = text
    for pattern in patterns:
        result = re.sub(pattern, "***TOKEN***", result, flags=re.IGNORECASE)

    return result


def mask_card_number(text: str) -> str:
    """Mask credit card numbers in text."""
    # Card number patterns (with or without separators)
    card_patterns = [
        r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",  # 16-digit cards
        r"\b\d{4}[-\s]?\d{6}[-\s]?\d{5}\b",  # 15-digit Amex
    ]

    result = text
    for pattern in card_patterns:
        result = re.sub(pattern, "***CARD***", result)

    return result


def mask_pii_in_text(text: str) -> str:
    """Comprehensive PII masking for log output."""
    if not isinstance(text, str):
        return str(text)

    result = text
    result = mask_email(result)
    result = mask_token(result)
    result = mask_card_number(result)

    return result


def mask_pii_in_dict(data: dict[str, Any]) -> dict[str, Any]:
    """Recursively mask PII in dictionary values."""
    if not isinstance(data, dict):
        return data

    result = {}
    for key, value in data.items():
        if isinstance(value, str):
            result[key] = mask_pii_in_text(value)
        elif isinstance(value, dict):
            result[key] = mask_pii_in_dict(value)
        elif isinstance(value, list):
            result[key] = [
                mask_pii_in_text(item) if isinstance(item, str) else item
                for item in value
            ]
        else:
            result[key] = value

    return result


def is_sensitive_key(key: str) -> bool:
    """Check if a key name indicates sensitive data."""
    sensitive_patterns = [
        "password",
        "secret",
        "token",
        "key",
        "auth",
        "signature",
        "credential",
        "private",
        "api_key",
        "signing_secret",
        "client_secret",
        "hmac_secret",
    ]

    key_lower = key.lower()
    return any(pattern in key_lower for pattern in sensitive_patterns)


def sanitize_log_data(data: Any) -> Any:
    """Sanitize data for safe logging by masking PII and sensitive values."""
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            if is_sensitive_key(key):
                result[key] = "***MASKED***"
            elif isinstance(value, str):
                result[key] = mask_pii_in_text(value)
            elif isinstance(value, dict):
                result[key] = sanitize_log_data(value)
            elif isinstance(value, list):
                result[key] = [sanitize_log_data(item) for item in value]
            else:
                result[key] = value
        return result
    elif isinstance(data, str):
        return mask_pii_in_text(data)
    elif isinstance(data, list):
        return [sanitize_log_data(item) for item in data]
    else:
        return data
