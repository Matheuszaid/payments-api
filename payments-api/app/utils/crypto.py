import hashlib
import hmac
import time


def constant_time_compare(a: str, b: str) -> bool:
    """
    Perform constant-time string comparison to prevent timing attacks.

    Args:
        a: First string to compare
        b: Second string to compare

    Returns:
        True if strings are equal, False otherwise
    """
    if len(a) != len(b):
        return False

    result = 0
    for x, y in zip(a, b, strict=False):
        result |= ord(x) ^ ord(y)
    return result == 0


def parse_stripe_signature(signature_header: str) -> tuple[int, str] | None:
    """
    Parse Stripe signature header to extract timestamp and signature.

    Args:
        signature_header: Stripe-Signature header value

    Returns:
        Tuple of (timestamp, signature) or None if invalid
    """
    if not signature_header:
        return None

    elements = signature_header.split(",")
    timestamp = None
    signature = None

    for element in elements:
        if "=" not in element:
            continue

        key, value = element.split("=", 1)
        if key == "t":
            try:
                timestamp = int(value)
            except ValueError:
                return None
        elif key == "v1" and signature is None:  # Take first v1 signature
            signature = value

    if timestamp is None or signature is None:
        return None

    return timestamp, signature


def verify_stripe_signature(
    payload: bytes, signature_header: str, signing_secret: str, tolerance: int = 300
) -> bool:
    """
    Verify Stripe webhook signature using official verification scheme.

    Args:
        payload: Raw webhook payload bytes
        signature_header: Stripe-Signature header value
        signing_secret: Stripe signing secret
        tolerance: Maximum age of webhook in seconds

    Returns:
        True if signature is valid, False otherwise
    """
    if not signing_secret:
        return False

    parsed = parse_stripe_signature(signature_header)
    if not parsed:
        return False

    timestamp, signature = parsed

    # Check timestamp tolerance
    current_time = int(time.time())
    if abs(current_time - timestamp) > tolerance:
        return False

    # Compute expected signature
    signed_payload = f"{timestamp}.{payload.decode('utf-8')}"
    expected_signature = hmac.new(
        signing_secret.encode("utf-8"), signed_payload.encode("utf-8"), hashlib.sha256
    ).hexdigest()

    # Constant-time comparison
    return constant_time_compare(signature, expected_signature)


def verify_demo_hmac(payload: bytes, signature: str, secret: str) -> bool:
    """
    Verify HMAC signature for demo/testing purposes.

    Args:
        payload: Raw payload bytes
        signature: HMAC signature to verify
        secret: HMAC secret

    Returns:
        True if signature is valid, False otherwise
    """
    if not secret or not signature:
        return False

    expected_signature = hmac.new(
        secret.encode("utf-8"), payload, hashlib.sha256
    ).hexdigest()

    return constant_time_compare(signature, expected_signature)
