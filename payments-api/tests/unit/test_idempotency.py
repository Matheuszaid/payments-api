from app.models import IdempotencyKey
from app.utils.idempotency import ensure_idempotency
from app.utils.idempotency import key_exists
from app.utils.idempotency import make_idempotency_key


class TestMakeIdempotencyKey:
    """Test idempotency key generation."""

    def test_stripe_key(self):
        """Test Stripe idempotency key format."""
        key = make_idempotency_key("stripe", "evt_123")
        assert key == "stripe:evt_123"

    def test_paypal_key(self):
        """Test PayPal idempotency key format."""
        key = make_idempotency_key("paypal", "WH-123")
        assert key == "paypal:WH-123"

    def test_different_providers_same_id(self):
        """Test that different providers with same ID create different keys."""
        stripe_key = make_idempotency_key("stripe", "123")
        paypal_key = make_idempotency_key("paypal", "123")
        assert stripe_key != paypal_key


async def test_ensure_idempotency_first_time(test_db):
    """Test idempotency check for first occurrence."""
    key = "stripe:evt_test_123"

    result = await ensure_idempotency(test_db, key)
    assert result is True

    # Verify key was stored
    stored_key = await key_exists(test_db, key)
    assert stored_key is True


async def test_ensure_idempotency_duplicate(test_db):
    """Test idempotency check for duplicate."""
    key = "stripe:evt_test_456"

    # First call should succeed
    result1 = await ensure_idempotency(test_db, key)
    assert result1 is True
    await test_db.commit()

    # Second call should return False (duplicate)
    result2 = await ensure_idempotency(test_db, key)
    assert result2 is False


async def test_key_exists_true(test_db):
    """Test key_exists for existing key."""
    key = "paypal:WH-test-789"

    # Insert key first
    idempotency_record = IdempotencyKey(key=key)
    test_db.add(idempotency_record)
    await test_db.commit()

    # Check existence
    exists = await key_exists(test_db, key)
    assert exists is True


async def test_key_exists_false(test_db):
    """Test key_exists for non-existing key."""
    key = "stripe:evt_nonexistent"

    exists = await key_exists(test_db, key)
    assert exists is False


async def test_concurrent_idempotency_checks(test_db):
    """Test concurrent idempotency checks (simulated)."""
    key = "stripe:evt_concurrent_test"

    # Simulate rapid duplicate requests
    # In real scenario, database constraints would handle this
    result1 = await ensure_idempotency(test_db, key)
    assert result1 is True
    await test_db.commit()

    result2 = await ensure_idempotency(test_db, key)
    assert result2 is False

    result3 = await ensure_idempotency(test_db, key)
    assert result3 is False
