import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import StaticPool

from app.config import Settings
from app.db import Base
from app.db import get_db
from app.main import create_app

# Test database settings
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="function")
async def test_db():
    """Create a test database session."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def test_db_for_concurrency():
    """Create a test database engine for concurrency tests with file-based SQLite."""
    import os
    import tempfile

    # Create a temporary SQLite file for this test
    temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    temp_db.close()
    temp_db_url = f"sqlite+aiosqlite:///{temp_db.name}"

    engine = create_async_engine(
        temp_db_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=True
    )

    try:
        yield async_session
    finally:
        await engine.dispose()
        # Clean up temporary file
        try:
            os.unlink(temp_db.name)
        except OSError:
            pass


@pytest.fixture
def test_settings(monkeypatch):
    """Create test settings with complete configuration."""
    # Set environment variables for test
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("DATABASE_URL", TEST_DATABASE_URL)
    monkeypatch.setenv("STRIPE_SIGNING_SECRET", "test_stripe_secret")
    monkeypatch.setenv("PAYPAL_MODE", "demo_hmac")
    monkeypatch.setenv("DEMO_HMAC_SECRET", "test_hmac_secret")
    monkeypatch.setenv("DLQ_BACKEND", "db")

    return Settings()


@pytest.fixture
def test_app(test_settings):
    """Create test app with settings override."""
    app = create_app(test_settings)
    return app


@pytest.fixture
def client(test_app, test_db):
    """Create a test client with database override."""

    async def override_get_db():
        yield test_db

    # Override database dependency
    test_app.dependency_overrides[get_db] = override_get_db

    # Create test client
    with TestClient(test_app) as test_client:
        yield test_client

    # Clean up after test
    test_app.dependency_overrides.clear()


@pytest.fixture
def stripe_webhook_payload():
    """Sample Stripe webhook payload."""
    return {
        "id": "evt_test_stripe_123",
        "type": "payment_intent.succeeded",
        "data": {"object": {"id": "pi_test_123", "amount": 2000, "currency": "usd"}},
        "created": 1677649200,
        "api_version": "2020-08-27",
    }


@pytest.fixture
def paypal_webhook_payload():
    """Sample PayPal webhook payload."""
    return {
        "id": "WH-test-paypal-123",
        "event_type": "PAYMENT.CAPTURE.COMPLETED",
        "resource": {
            "id": "CAPTURE-test-123",
            "amount": {"currency_code": "USD", "value": "20.00"},
        },
        "create_time": "2023-03-01T10:00:00Z",
        "event_version": "1.0",
    }
