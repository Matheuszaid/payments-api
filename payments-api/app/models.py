from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db import Base


class IdempotencyKey(Base):
    """Track idempotency keys to prevent duplicate processing."""

    __tablename__ = "idempotency_keys"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (Index("idx_idempotency_key", "key"),)


class PaymentEvent(Base):
    """Store webhook events from payment providers."""

    __tablename__ = "payment_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    event_id: Mapped[str] = mapped_column(String(255), nullable=False)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    payload_json: Mapped[str] = mapped_column(Text, nullable=False)
    received_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("provider", "event_id", name="uq_provider_event_id"),
        Index("idx_provider_event_id", "provider", "event_id"),
        Index("idx_received_at", "received_at"),
        Index("idx_event_type", "event_type"),
    )


class DLQMessage(Base):
    """Dead Letter Queue for failed webhook processing."""

    __tablename__ = "dlq_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    event_id: Mapped[str] = mapped_column(String(255), nullable=False)
    payload_json: Mapped[str] = mapped_column(Text, nullable=False)
    error_kind: Mapped[str] = mapped_column(String(100), nullable=False)
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    next_retry_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("idx_next_retry_at", "next_retry_at"),
        Index("idx_provider_event_id_dlq", "provider", "event_id"),
    )


class ReconciliationLog(Base):
    """Track reconciliation activities and results."""

    __tablename__ = "reconciliation_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider: Mapped[str | None] = mapped_column(String(50), nullable=True)
    event_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    details_json: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("idx_reconciliation_created_at", "created_at"),
        Index("idx_reconciliation_status", "status"),
    )
