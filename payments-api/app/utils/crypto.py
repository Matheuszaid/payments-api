import hashlib
import hmac
import time


def constant_time_compare(a: str, b: str) -> bool:
    """Constant-time string comparison."""
    if len(a) != len(b):
        return False

    result = 0
    for x, y in zip(a, b, strict=False):
        result |= ord(x) ^ ord(y)
    return result == 0


def parse_stripe_signature(signature_header: str) -> tuple[int, str] | None:
    """Parse Stripe signature header."""
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
    """Verify Stripe webhook signature."""
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
    """Verify HMAC signature for demo/testing."""
    if not secret or not signature:
        return False

    expected_signature = hmac.new(
        secret.encode("utf-8"), payload, hashlib.sha256
    ).hexdigest()

    return constant_time_compare(signature, expected_signature)
