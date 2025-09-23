from typing import Literal

from pydantic import ConfigDict
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings."""

    # Application
    app_env: Literal["dev", "test", "prod"] = Field(default="dev", alias="APP_ENV")
    app_port: int = Field(default=8065, alias="APP_PORT")
    database_url: str = Field(
        default="sqlite+aiosqlite:///./payments.db", alias="DATABASE_URL"
    )

    # Security
    max_request_size: int = Field(default=1048576, alias="MAX_REQUEST_SIZE")  # 1MB
    stripe_timestamp_tolerance: int = Field(
        default=300, alias="STRIPE_TIMESTAMP_TOLERANCE"
    )  # 5 minutes

    # Stripe
    stripe_signing_secret: str = Field(default="", alias="STRIPE_SIGNING_SECRET")

    # PayPal
    paypal_mode: Literal["live", "sandbox", "demo_hmac"] = Field(
        default="sandbox", alias="PAYPAL_MODE"
    )
    paypal_webhook_id: str = Field(default="", alias="PAYPAL_WEBHOOK_ID")
    paypal_client_id: str = Field(default="", alias="PAYPAL_CLIENT_ID")
    paypal_client_secret: str = Field(default="", alias="PAYPAL_CLIENT_SECRET")
    demo_hmac_secret: str = Field(default="", alias="DEMO_HMAC_SECRET")

    # DLQ
    dlq_backend: Literal["db", "redis"] = Field(default="db", alias="DLQ_BACKEND")
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")

    model_config = ConfigDict(env_file=".env", case_sensitive=False, extra="allow")

    def get_masked_config(self) -> dict:
        """Get configuration with sensitive values masked for logging."""
        config = self.model_dump()
        sensitive_keys = [
            "stripe_signing_secret",
            "paypal_client_secret",
            "demo_hmac_secret",
            "redis_url",
        ]

        for key in sensitive_keys:
            if config.get(key):
                config[key] = "***MASKED***"

        return config


def get_settings() -> Settings:
    """Get application settings singleton."""
    return Settings()


def settings_dep() -> Settings:
    """Settings dependency for FastAPI DI."""
    return get_settings()
