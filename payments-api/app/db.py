from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings


class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


class DatabaseManager:
    """Database connection and session management."""

    def __init__(self):
        self.settings = get_settings()
        self.engine = create_async_engine(
            self.settings.database_url, echo=self.settings.app_env == "dev"
        )
        self.async_session = async_sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def create_tables(self):
        """Create all database tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def close(self):
        """Close database engine."""
        await self.engine.dispose()

    async def get_session(self) -> AsyncSession:
        """Get async database session."""
        async with self.async_session() as session:
            try:
                yield session
            finally:
                await session.close()

    async def health_check(self) -> bool:
        """Check if database is accessible."""
        try:
            async with self.engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            return True
        except Exception:
            return False


# Global database manager instance
db_manager = DatabaseManager()


async def get_db() -> AsyncSession:
    """Dependency for getting database session."""
    async for session in db_manager.get_session():
        yield session
