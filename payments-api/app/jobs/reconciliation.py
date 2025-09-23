import json
import logging
from datetime import UTC
from datetime import datetime
from datetime import timedelta
from typing import Any

from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.db import db_manager
from app.models import PaymentEvent
from app.models import ReconciliationLog

logger = logging.getLogger(__name__)


class ReconciliationJob:
    """Scheduled job for payment events reconciliation."""

    def __init__(self):
        self.settings = get_settings()

    async def run_reconciliation(self, hours_back: int = 24) -> dict[str, Any]:
        """
        Run reconciliation for events in the specified time window.

        Args:
            hours_back: Number of hours to look back from now

        Returns:
            Reconciliation summary data
        """
        end_time = datetime.now(UTC)
        start_time = end_time - timedelta(hours=hours_back)

        logger.info(f"Starting reconciliation from {start_time} to {end_time}")

        async for session in db_manager.get_session():
            try:
                # Get event counts by provider
                events_by_provider = await self._get_events_by_provider(
                    session, start_time, end_time
                )

                # Get event counts by type
                events_by_type = await self._get_events_by_type(
                    session, start_time, end_time
                )

                # Get total event count
                total_events = await self._get_total_events(
                    session, start_time, end_time
                )

                # Detect anomalies
                anomalies = await self._detect_anomalies(session, start_time, end_time)

                # Create summary
                summary = {
                    "period_start": start_time,
                    "period_end": end_time,
                    "total_events": total_events,
                    "events_by_provider": events_by_provider,
                    "events_by_type": events_by_type,
                    "anomalies": anomalies,
                    "generated_at": datetime.now(UTC),
                }

                # Log reconciliation result
                await self._log_reconciliation(session, summary)

                logger.info(
                    f"Reconciliation completed: {total_events} events processed",
                    extra=summary,
                )

                return summary

            except Exception as e:
                logger.error(f"Reconciliation failed: {e}")
                raise

    async def _get_events_by_provider(
        self, session: AsyncSession, start_time: datetime, end_time: datetime
    ) -> dict[str, int]:
        """Get event counts grouped by provider."""
        stmt = (
            select(PaymentEvent.provider, func.count(PaymentEvent.id))
            .where(
                and_(
                    PaymentEvent.received_at >= start_time,
                    PaymentEvent.received_at <= end_time,
                )
            )
            .group_by(PaymentEvent.provider)
        )

        result = await session.execute(stmt)
        return dict(result.fetchall())

    async def _get_events_by_type(
        self, session: AsyncSession, start_time: datetime, end_time: datetime
    ) -> dict[str, int]:
        """Get event counts grouped by event type."""
        stmt = (
            select(PaymentEvent.event_type, func.count(PaymentEvent.id))
            .where(
                and_(
                    PaymentEvent.received_at >= start_time,
                    PaymentEvent.received_at <= end_time,
                )
            )
            .group_by(PaymentEvent.event_type)
        )

        result = await session.execute(stmt)
        return dict(result.fetchall())

    async def _get_total_events(
        self, session: AsyncSession, start_time: datetime, end_time: datetime
    ) -> int:
        """Get total event count for the period."""
        stmt = select(func.count(PaymentEvent.id)).where(
            and_(
                PaymentEvent.received_at >= start_time,
                PaymentEvent.received_at <= end_time,
            )
        )

        result = await session.execute(stmt)
        return result.scalar() or 0

    async def _detect_anomalies(
        self, session: AsyncSession, start_time: datetime, end_time: datetime
    ) -> list[dict[str, Any]]:
        """Detect potential anomalies in the data."""
        anomalies = []

        # Check for duplicate event IDs across providers
        stmt = (
            select(PaymentEvent.event_id, func.count(PaymentEvent.id))
            .where(
                and_(
                    PaymentEvent.received_at >= start_time,
                    PaymentEvent.received_at <= end_time,
                )
            )
            .group_by(PaymentEvent.event_id)
            .having(func.count(PaymentEvent.id) > 1)
        )

        result = await session.execute(stmt)
        duplicates = result.fetchall()

        if duplicates:
            anomalies.append(
                {
                    "type": "duplicate_event_ids",
                    "description": "Event IDs appearing multiple times",
                    "count": len(duplicates),
                    "details": [
                        {"event_id": event_id, "count": count}
                        for event_id, count in duplicates
                    ],
                }
            )

        # Check for unusual event type frequencies
        # (This is a simplified check - in practice, you'd have baseline metrics)
        events_by_type = await self._get_events_by_type(session, start_time, end_time)
        for event_type, count in events_by_type.items():
            if count > 1000:  # Arbitrary threshold for demo
                anomalies.append(
                    {
                        "type": "high_frequency_event",
                        "description": f"Unusually high frequency for event type: {event_type}",
                        "event_type": event_type,
                        "count": count,
                    }
                )

        return anomalies

    async def _log_reconciliation(self, session: AsyncSession, summary: dict[str, Any]):
        """Log reconciliation results to the database."""
        log_entry = ReconciliationLog(
            provider=None,  # Summary covers all providers
            event_id=None,
            status="completed",
            details_json=json.dumps(summary, default=str),
        )

        session.add(log_entry)
        await session.commit()


# Global reconciliation job instance
reconciliation_job = ReconciliationJob()
