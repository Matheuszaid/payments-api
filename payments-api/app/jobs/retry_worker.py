import asyncio
import logging
import random
from datetime import UTC
from datetime import datetime
from datetime import timedelta

from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import db_manager
from app.models import DLQMessage

logger = logging.getLogger(__name__)


class RetryWorker:
    """Background worker to process DLQ messages with retry logic."""

    def __init__(self, max_concurrent: int = 5):
        self.max_concurrent = max_concurrent
        self.running = False
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def start(self):
        """Start the retry worker."""
        self.running = True
        logger.info("Retry worker started")

        while self.running:
            try:
                await self._process_due_messages()
                await asyncio.sleep(30)  # Check every 30 seconds
            except Exception as e:
                logger.error(f"Retry worker error: {e}")
                await asyncio.sleep(60)  # Back off on error

    async def stop(self):
        """Stop the retry worker."""
        self.running = False
        logger.info("Retry worker stopped")

    async def _process_due_messages(self):
        """Process messages that are due for retry."""
        async for session in db_manager.get_session():
            try:
                # Get messages due for retry
                now = datetime.now(UTC)
                stmt = (
                    select(DLQMessage)
                    .where(
                        and_(
                            DLQMessage.next_retry_at <= now,
                            DLQMessage.attempts < 5,  # Max retry attempts
                        )
                    )
                    .limit(10)
                )

                result = await session.execute(stmt)
                messages = result.scalars().all()

                if messages:
                    logger.info(f"Processing {len(messages)} DLQ messages")

                # Process messages concurrently
                tasks = [
                    self._process_message(message, session) for message in messages
                ]
                await asyncio.gather(*tasks, return_exceptions=True)

            except Exception as e:
                logger.error(f"Error processing DLQ messages: {e}")

    async def _process_message(self, message: DLQMessage, session: AsyncSession):
        """Process a single DLQ message."""
        async with self.semaphore:
            try:
                # Simulate processing (in real implementation, this would
                # retry the original webhook processing)
                success = await self._simulate_processing(message)

                if success:
                    # Remove from DLQ on success
                    await session.delete(message)
                    logger.info(f"Successfully processed DLQ message: {message.id}")
                else:
                    # Update retry info
                    message.attempts += 1
                    message.next_retry_at = self._calculate_next_retry(message.attempts)
                    logger.warning(
                        f"Failed to process DLQ message {message.id}, "
                        f"attempt {message.attempts}, next retry: {message.next_retry_at}"
                    )

                await session.commit()

            except Exception as e:
                await session.rollback()
                logger.error(f"Error processing DLQ message {message.id}: {e}")

    async def _simulate_processing(self, message: DLQMessage) -> bool:
        """
        Simulate processing of a DLQ message.
        In real implementation, this would retry the original webhook processing.
        """
        # Simulate some processing time
        await asyncio.sleep(0.1)

        # Simulate 70% success rate for demonstration
        return random.random() < 0.7

    def _calculate_next_retry(self, attempts: int) -> datetime:
        """
        Calculate next retry time using exponential backoff with jitter.

        Args:
            attempts: Number of previous attempts

        Returns:
            Next retry datetime
        """
        # Exponential backoff: 2^attempts minutes with max of 60 minutes
        base_delay = min(2**attempts, 60) * 60  # Convert to seconds

        # Add jitter (±25%)
        jitter = base_delay * 0.25 * (random.random() * 2 - 1)
        total_delay = base_delay + jitter

        return datetime.now(UTC) + timedelta(seconds=total_delay)


async def add_to_dlq(
    session: AsyncSession,
    provider: str,
    event_id: str,
    payload_json: str,
    error_kind: str,
) -> DLQMessage:
    """
    Add a failed message to the DLQ.

    Args:
        session: Database session
        provider: Payment provider name
        event_id: Event ID from the provider
        payload_json: JSON payload that failed
        error_kind: Type of error that occurred

    Returns:
        Created DLQMessage
    """
    dlq_message = DLQMessage(
        provider=provider,
        event_id=event_id,
        payload_json=payload_json,
        error_kind=error_kind,
        attempts=0,
        next_retry_at=datetime.now(UTC)
        + timedelta(minutes=1),  # First retry in 1 minute
    )

    session.add(dlq_message)
    await session.flush()

    logger.info(
        f"Added message to DLQ: {provider}:{event_id}",
        extra={
            "provider": provider,
            "event_id": event_id,
            "error_kind": error_kind,
            "dlq_id": dlq_message.id,
        },
    )

    return dlq_message


# Global retry worker instance
retry_worker = RetryWorker()
