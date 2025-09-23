import types
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Base
from app.db import DatabaseManager
from app.db import db_manager
from app.db import get_db


class TestDatabaseManager:
    """Test cases for DatabaseManager class."""

    def test_database_manager_initialization(self):
        """Test DatabaseManager initialization."""
        with patch("app.db.get_settings") as mock_settings:
            mock_settings.return_value.database_url = "sqlite+aiosqlite:///:memory:"
            mock_settings.return_value.app_env = "test"

            manager = DatabaseManager()

            assert manager.settings is not None
            assert manager.engine is not None
            assert manager.async_session is not None

    def test_database_manager_echo_in_dev(self):
        """Test that echo is enabled in dev environment."""
        with patch("app.db.get_settings") as mock_settings:
            mock_settings.return_value.database_url = "sqlite+aiosqlite:///:memory:"
            mock_settings.return_value.app_env = "dev"

            with patch("app.db.create_async_engine") as mock_create_engine:
                DatabaseManager()

                # Verify echo=True was passed when app_env is "dev"
                call_args = mock_create_engine.call_args
                assert call_args[1]["echo"] is True

    def test_database_manager_no_echo_in_prod(self):
        """Test that echo is disabled in production environment."""
        with patch("app.db.get_settings") as mock_settings:
            mock_settings.return_value.database_url = "sqlite+aiosqlite:///:memory:"
            mock_settings.return_value.app_env = "prod"

            with patch("app.db.create_async_engine") as mock_create_engine:
                DatabaseManager()

                # Verify echo=False was passed when app_env is not "dev"
                call_args = mock_create_engine.call_args
                assert call_args[1]["echo"] is False

    @pytest.mark.asyncio
    async def test_create_tables(self):
        """Test create_tables method."""
        with patch("app.db.get_settings") as mock_settings:
            mock_settings.return_value.database_url = "sqlite+aiosqlite:///:memory:"
            mock_settings.return_value.app_env = "test"

            with patch("app.db.create_async_engine") as mock_create_engine:
                # Create properly structured mock engine
                mock_engine = MagicMock()
                mock_conn = AsyncMock()

                # Mock the async context manager behavior
                async_context = AsyncMock()
                async_context.__aenter__ = AsyncMock(return_value=mock_conn)
                async_context.__aexit__ = AsyncMock(return_value=None)
                mock_engine.begin.return_value = async_context

                mock_create_engine.return_value = mock_engine

                manager = DatabaseManager()
                await manager.create_tables()

                # Verify run_sync was called with Base.metadata.create_all
                mock_conn.run_sync.assert_called_once_with(Base.metadata.create_all)

    @pytest.mark.asyncio
    async def test_close(self):
        """Test close method."""
        with patch("app.db.get_settings") as mock_settings:
            mock_settings.return_value.database_url = "sqlite+aiosqlite:///:memory:"
            mock_settings.return_value.app_env = "test"

            with patch("app.db.create_async_engine") as mock_create_engine:
                mock_engine = AsyncMock()
                mock_create_engine.return_value = mock_engine

                manager = DatabaseManager()
                await manager.close()

                # Verify engine.dispose was called
                mock_engine.dispose.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_session(self):
        """Test get_session method."""
        with patch("app.db.get_settings") as mock_settings:
            mock_settings.return_value.database_url = "sqlite+aiosqlite:///:memory:"
            mock_settings.return_value.app_env = "test"

            with patch("app.db.create_async_engine") as mock_create_engine:
                with patch("app.db.async_sessionmaker") as mock_sessionmaker:
                    mock_engine = AsyncMock()
                    mock_create_engine.return_value = mock_engine

                    # Mock the session properly
                    mock_session = AsyncMock(spec=AsyncSession)
                    mock_session.close = AsyncMock()

                    # Mock the sessionmaker to create a proper async context manager
                    mock_sessionmaker_instance = MagicMock()

                    # Create a mock for the async context manager
                    class MockAsyncSession:
                        def __init__(self):
                            pass

                        async def __aenter__(self):
                            return mock_session

                        async def __aexit__(self, exc_type, exc_val, exc_tb):
                            return None

                    mock_sessionmaker_instance.return_value = MockAsyncSession()
                    mock_sessionmaker.return_value = mock_sessionmaker_instance

                    manager = DatabaseManager()

                    # Test the async generator - need to complete the iteration
                    sessions = []
                    async_gen = manager.get_session()
                    try:
                        async for session in async_gen:
                            sessions.append(session)
                            break  # Only test one iteration
                    finally:
                        await async_gen.aclose()

                    assert len(sessions) == 1
                    assert sessions[0] == mock_session

                    # Verify session.close was called in finally block
                    mock_session.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_session_exception_handling(self):
        """Test get_session handles exceptions and still closes session."""
        with patch("app.db.get_settings") as mock_settings:
            mock_settings.return_value.database_url = "sqlite+aiosqlite:///:memory:"
            mock_settings.return_value.app_env = "test"

            with patch("app.db.create_async_engine") as mock_create_engine:
                with patch("app.db.async_sessionmaker") as mock_sessionmaker:
                    mock_engine = AsyncMock()
                    mock_create_engine.return_value = mock_engine

                    # Mock the session properly
                    mock_session = AsyncMock(spec=AsyncSession)
                    mock_session.close = AsyncMock()

                    # Mock the sessionmaker to create a proper async context manager
                    mock_sessionmaker_instance = MagicMock()

                    # Create a mock for the async context manager
                    class MockAsyncSession:
                        def __init__(self):
                            pass

                        async def __aenter__(self):
                            return mock_session

                        async def __aexit__(self, exc_type, exc_val, exc_tb):
                            return None

                    mock_sessionmaker_instance.return_value = MockAsyncSession()
                    mock_sessionmaker.return_value = mock_sessionmaker_instance

                    manager = DatabaseManager()

                    # Test exception handling
                    async_gen = manager.get_session()
                    try:
                        async for session in async_gen:
                            assert session == mock_session
                            raise Exception("Test exception")
                    except Exception:
                        pass  # Expected
                    finally:
                        await async_gen.aclose()

                    # Verify session.close was still called despite exception
                    mock_session.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_health_check_success(self):
        """Test successful health check."""
        with patch("app.db.get_settings") as mock_settings:
            mock_settings.return_value.database_url = "sqlite+aiosqlite:///:memory:"
            mock_settings.return_value.app_env = "test"

            with patch("app.db.create_async_engine") as mock_create_engine:
                # Create properly structured mock engine
                mock_engine = MagicMock()
                mock_conn = AsyncMock()

                # Mock the async context manager behavior
                async_context = AsyncMock()
                async_context.__aenter__ = AsyncMock(return_value=mock_conn)
                async_context.__aexit__ = AsyncMock(return_value=None)
                mock_engine.begin.return_value = async_context

                mock_create_engine.return_value = mock_engine

                manager = DatabaseManager()
                result = await manager.health_check()

                assert result is True
                mock_conn.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_health_check_failure(self):
        """Test health check with database connection failure."""
        with patch("app.db.get_settings") as mock_settings:
            mock_settings.return_value.database_url = "sqlite+aiosqlite:///:memory:"
            mock_settings.return_value.app_env = "test"

            with patch("app.db.create_async_engine") as mock_create_engine:
                mock_engine = MagicMock()
                mock_engine.begin.side_effect = Exception("Connection failed")
                mock_create_engine.return_value = mock_engine

                manager = DatabaseManager()
                result = await manager.health_check()

                assert result is False

    @pytest.mark.asyncio
    async def test_health_check_execute_failure(self):
        """Test health check with execute failure."""
        with patch("app.db.get_settings") as mock_settings:
            mock_settings.return_value.database_url = "sqlite+aiosqlite:///:memory:"
            mock_settings.return_value.app_env = "test"

            with patch("app.db.create_async_engine") as mock_create_engine:
                # Create properly structured mock engine
                mock_engine = MagicMock()
                mock_conn = AsyncMock()
                mock_conn.execute.side_effect = Exception("Execute failed")

                # Mock the async context manager behavior
                async_context = AsyncMock()
                async_context.__aenter__ = AsyncMock(return_value=mock_conn)
                async_context.__aexit__ = AsyncMock(return_value=None)
                mock_engine.begin.return_value = async_context

                mock_create_engine.return_value = mock_engine

                manager = DatabaseManager()
                result = await manager.health_check()

                assert result is False


class TestBase:
    """Test cases for Base class."""

    def test_base_class_exists(self):
        """Test that Base class is properly defined."""
        assert Base is not None
        assert hasattr(Base, "metadata")
        assert hasattr(Base, "registry")


class TestGlobalDatabaseManager:
    """Test cases for global database manager instance."""

    def test_global_db_manager_exists(self):
        """Test that global db_manager instance exists."""
        assert db_manager is not None
        assert isinstance(db_manager, DatabaseManager)

    def test_global_db_manager_singleton(self):
        """Test that we get the same instance."""
        from app.db import db_manager as db_manager2

        assert db_manager is db_manager2


class TestGetDbDependency:
    """Test cases for get_db dependency function."""

    @pytest.mark.asyncio
    async def test_get_db_function(self):
        """Test get_db dependency function."""
        # Mock the global db_manager
        with patch("app.db.db_manager") as mock_db_manager:
            mock_session = AsyncMock(spec=AsyncSession)

            # Mock the get_session async generator
            async def mock_get_session():
                yield mock_session

            mock_db_manager.get_session = mock_get_session

            # Test the get_db function
            sessions = []
            async for session in get_db():
                sessions.append(session)

            assert len(sessions) == 1
            assert sessions[0] == mock_session

    @pytest.mark.asyncio
    async def test_get_db_yields_session(self):
        """Test that get_db properly yields database session."""
        # This is more of an integration test, but we'll mock to avoid actual DB
        with patch("app.db.db_manager") as mock_db_manager:
            mock_session = Mock(spec=AsyncSession)

            # Mock the async generator behavior
            async def mock_get_session():
                yield mock_session

            mock_db_manager.get_session = mock_get_session

            # Collect all yielded sessions
            sessions = []
            async for session in get_db():
                sessions.append(session)

            assert len(sessions) == 1
            assert sessions[0] == mock_session

    @pytest.mark.asyncio
    async def test_get_db_async_generator(self):
        """Test that get_db is an async generator."""
        # get_db should return an async generator
        result = get_db()
        assert isinstance(result, types.AsyncGeneratorType)

        # Clean up the generator
        await result.aclose()


class TestDatabaseIntegration:
    """Integration test cases for database components."""

    @pytest.mark.asyncio
    async def test_database_manager_with_real_settings(self):
        """Test DatabaseManager with actual settings object."""
        # Use actual settings but mock the database engine creation
        with patch("app.db.create_async_engine") as mock_create_engine:
            with patch("app.db.async_sessionmaker") as mock_sessionmaker:
                mock_engine = Mock()
                mock_create_engine.return_value = mock_engine

                DatabaseManager()

                # Verify engine was created with settings
                mock_create_engine.assert_called_once()
                mock_sessionmaker.assert_called_once()

                # Verify sessionmaker was called with correct parameters
                call_args = mock_sessionmaker.call_args
                assert call_args[1]["bind"] == mock_engine
                assert call_args[1]["class_"] == AsyncSession
                assert call_args[1]["expire_on_commit"] is False
