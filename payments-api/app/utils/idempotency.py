import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import IdempotencyKey

logger = logging.getLogger(__name__)


async def ensure_idempotency(db: AsyncSession, key: str) -> bool:
    """
    Ensure idempotency by checking if key already exists.

    This function uses a try-catch approach with savepoints for
    idempotency key insertion in concurrent environments.

    Args:
        db: Database session
        key: Idempotency key to check/insert

    Returns:
        True if this is the first time seeing this key, False if duplicate
    """
    # First try a simple check
    result = await db.execute(select(IdempotencyKey).where(IdempotencyKey.key == key))
    existing = result.scalar_one_or_none()

    if existing:
        logger.info(f"Duplicate idempotency key detected: {key}")
        return False

    # Use a savepoint to safely attempt insertion
    savepoint = await db.begin_nested()
    try:
        # Try to insert the key
        idempotency_record = IdempotencyKey(key=key)
        db.add(idempotency_record)
        await db.flush()  # Flush to trigger constraint check
        await savepoint.commit()
        return True

    except IntegrityError:
        # Key was inserted by another concurrent request between check and insert
        await savepoint.rollback()
        logger.info(f"Duplicate idempotency key detected (race condition): {key}")
        return False


async def key_exists(db: AsyncSession, key: str) -> bool:
    """
    Check if idempotency key exists without trying to insert.

    Args:
        db: Database session
        key: Idempotency key to check

    Returns:
        True if key exists, False otherwise
    """
    result = await db.execute(select(IdempotencyKey).where(IdempotencyKey.key == key))
    return result.scalar_one_or_none() is not None


def make_idempotency_key(provider: str, event_id: str) -> str:
    """
    Create standardized idempotency key.

    Args:
        provider: Payment provider name (stripe, paypal)
        event_id: Event ID from the provider

    Returns:
        Formatted idempotency key
    """
    return f"{provider}:{event_id}"
