from datetime import datetime
from typing import Any

from pydantic import BaseModel
from pydantic import Field


class WebhookResponse(BaseModel):
    """Standard webhook response format."""

    status: str = Field(description="Processing status")
    message: str = Field(description="Response message")
    event_id: str | None = Field(None, description="Event ID if available")


class StripeWebhookEvent(BaseModel):
    """Stripe webhook event structure."""

    id: str = Field(description="Stripe event ID")
    type: str = Field(description="Event type")
    data: dict[str, Any] = Field(description="Event data")
    created: int = Field(description="Event creation timestamp")
    api_version: str | None = Field(None, description="API version")


class PayPalWebhookEvent(BaseModel):
    """PayPal webhook event structure."""

    id: str = Field(description="PayPal event ID")
    event_type: str = Field(description="Event type")
    resource: dict[str, Any] = Field(description="Event resource data")
    create_time: str = Field(description="Event creation time")
    event_version: str | None = Field(None, description="Event version")


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(description="Service status")
    timestamp: datetime = Field(description="Check timestamp")
    version: str = Field(description="API version")


class ReadinessResponse(BaseModel):
    """Readiness check response."""

    status: str = Field(description="Service readiness status")
    checks: dict[str, bool] = Field(description="Individual check results")
    timestamp: datetime = Field(description="Check timestamp")


class MetricsResponse(BaseModel):
    """Metrics response."""

    counters: dict[str, int] = Field(description="Event counters")
    timestamp: datetime = Field(description="Metrics timestamp")


class ReconciliationSummary(BaseModel):
    """Reconciliation summary response."""

    period_start: datetime = Field(description="Summary period start")
    period_end: datetime = Field(description="Summary period end")
    total_events: int = Field(description="Total events processed")
    events_by_provider: dict[str, int] = Field(description="Events grouped by provider")
    events_by_type: dict[str, int] = Field(description="Events grouped by type")
    anomalies: list = Field(description="Detected anomalies")
    generated_at: datetime = Field(description="Summary generation time")
