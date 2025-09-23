import json
from datetime import UTC
from datetime import datetime
from datetime import timedelta
from unittest.mock import AsyncMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest

from app.jobs.reconciliation import ReconciliationJob
from app.models import ReconciliationLog


class TestReconciliationJob:
    """Test cases for ReconciliationJob."""

    @pytest.fixture
    def reconciliation_job(self):
        """Create a ReconciliationJob instance for testing."""
        return ReconciliationJob()

    @pytest.fixture
    def mock_session(self):
        """Create a mock database session."""
        session = AsyncMock()
        session.execute = AsyncMock()
        session.add = Mock()
        session.commit = AsyncMock()
        return session

    @pytest.fixture
    def sample_events_data(self):
        """Sample data for testing."""
        return {
            "events_by_provider": {"stripe": 10, "paypal": 5},
            "events_by_type": {"payment.completed": 12, "payment.failed": 3},
            "total_events": 15,
            "duplicates": [("event_123", 2), ("event_456", 3)],
        }

    @pytest.mark.asyncio
    async def test_run_reconciliation_success(
        self, reconciliation_job, mock_session, sample_events_data
    ):
        """Test successful reconciliation run."""

        # Mock db_manager.get_session() as async generator
        async def mock_get_session():
            yield mock_session

        with patch("app.jobs.reconciliation.db_manager") as mock_db_manager:
            mock_db_manager.get_session = mock_get_session

            # Mock internal methods
            reconciliation_job._get_events_by_provider = AsyncMock(
                return_value=sample_events_data["events_by_provider"]
            )
            reconciliation_job._get_events_by_type = AsyncMock(
                return_value=sample_events_data["events_by_type"]
            )
            reconciliation_job._get_total_events = AsyncMock(
                return_value=sample_events_data["total_events"]
            )
            reconciliation_job._detect_anomalies = AsyncMock(return_value=[])
            reconciliation_job._log_reconciliation = AsyncMock()

            # Run reconciliation
            result = await reconciliation_job.run_reconciliation(hours_back=24)

            # Verify result structure
            assert "period_start" in result
            assert "period_end" in result
            assert "total_events" in result
            assert "events_by_provider" in result
            assert "events_by_type" in result
            assert "anomalies" in result
            assert "generated_at" in result

            # Verify data
            assert result["total_events"] == 15
            assert (
                result["events_by_provider"] == sample_events_data["events_by_provider"]
            )
            assert result["events_by_type"] == sample_events_data["events_by_type"]

            # Verify time range
            end_time = result["period_end"]
            start_time = result["period_start"]
            assert end_time - start_time == timedelta(hours=24)

            # Verify methods were called
            reconciliation_job._get_events_by_provider.assert_called_once()
            reconciliation_job._get_events_by_type.assert_called_once()
            reconciliation_job._get_total_events.assert_called_once()
            reconciliation_job._detect_anomalies.assert_called_once()
            reconciliation_job._log_reconciliation.assert_called_once()

    @pytest.mark.asyncio
    async def test_run_reconciliation_with_custom_hours(
        self, reconciliation_job, mock_session
    ):
        """Test reconciliation with custom hours_back parameter."""

        # Mock db_manager.get_session() as async generator
        async def mock_get_session():
            yield mock_session

        with patch("app.jobs.reconciliation.db_manager") as mock_db_manager:
            mock_db_manager.get_session = mock_get_session

            # Mock internal methods
            reconciliation_job._get_events_by_provider = AsyncMock(return_value={})
            reconciliation_job._get_events_by_type = AsyncMock(return_value={})
            reconciliation_job._get_total_events = AsyncMock(return_value=0)
            reconciliation_job._detect_anomalies = AsyncMock(return_value=[])
            reconciliation_job._log_reconciliation = AsyncMock()

            # Run with custom hours
            result = await reconciliation_job.run_reconciliation(hours_back=12)

            # Verify time range
            end_time = result["period_end"]
            start_time = result["period_start"]
            assert end_time - start_time == timedelta(hours=12)

    @pytest.mark.asyncio
    async def test_run_reconciliation_handles_exception(
        self, reconciliation_job, mock_session
    ):
        """Test reconciliation handles exceptions properly."""

        # Mock db_manager.get_session() as async generator
        async def mock_get_session():
            yield mock_session

        with patch("app.jobs.reconciliation.db_manager") as mock_db_manager:
            mock_db_manager.get_session = mock_get_session

            # Mock method to raise exception
            reconciliation_job._get_events_by_provider = AsyncMock(
                side_effect=Exception("Database error")
            )

            # Verify exception is raised
            with pytest.raises(Exception, match="Database error"):
                await reconciliation_job.run_reconciliation()

    @pytest.mark.asyncio
    async def test_get_events_by_provider(self, reconciliation_job, mock_session):
        """Test _get_events_by_provider method."""
        # Mock query result
        mock_result = Mock()
        mock_result.fetchall.return_value = [("stripe", 10), ("paypal", 5)]
        mock_session.execute.return_value = mock_result

        start_time = datetime.now(UTC) - timedelta(hours=24)
        end_time = datetime.now(UTC)

        result = await reconciliation_job._get_events_by_provider(
            mock_session, start_time, end_time
        )

        assert result == {"stripe": 10, "paypal": 5}
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_events_by_type(self, reconciliation_job, mock_session):
        """Test _get_events_by_type method."""
        # Mock query result
        mock_result = Mock()
        mock_result.fetchall.return_value = [
            ("payment.completed", 12),
            ("payment.failed", 3),
        ]
        mock_session.execute.return_value = mock_result

        start_time = datetime.now(UTC) - timedelta(hours=24)
        end_time = datetime.now(UTC)

        result = await reconciliation_job._get_events_by_type(
            mock_session, start_time, end_time
        )

        assert result == {"payment.completed": 12, "payment.failed": 3}
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_total_events(self, reconciliation_job, mock_session):
        """Test _get_total_events method."""
        # Mock query result
        mock_result = Mock()
        mock_result.scalar.return_value = 15
        mock_session.execute.return_value = mock_result

        start_time = datetime.now(UTC) - timedelta(hours=24)
        end_time = datetime.now(UTC)

        result = await reconciliation_job._get_total_events(
            mock_session, start_time, end_time
        )

        assert result == 15
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_total_events_no_results(self, reconciliation_job, mock_session):
        """Test _get_total_events method when no results."""
        # Mock query result with None
        mock_result = Mock()
        mock_result.scalar.return_value = None
        mock_session.execute.return_value = mock_result

        start_time = datetime.now(UTC) - timedelta(hours=24)
        end_time = datetime.now(UTC)

        result = await reconciliation_job._get_total_events(
            mock_session, start_time, end_time
        )

        assert result == 0

    @pytest.mark.asyncio
    async def test_detect_anomalies_with_duplicates(
        self, reconciliation_job, mock_session
    ):
        """Test _detect_anomalies method with duplicate event IDs."""
        # Mock duplicate detection query
        duplicate_result = Mock()
        duplicate_result.fetchall.return_value = [("event_123", 2), ("event_456", 3)]

        # Mock event type query for anomaly detection
        reconciliation_job._get_events_by_type = AsyncMock(
            return_value={"payment.completed": 500}
        )

        # Configure session.execute to return different results for different calls
        call_count = 0

        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return duplicate_result
            return Mock()

        mock_session.execute.side_effect = side_effect

        start_time = datetime.now(UTC) - timedelta(hours=24)
        end_time = datetime.now(UTC)

        result = await reconciliation_job._detect_anomalies(
            mock_session, start_time, end_time
        )

        assert len(result) == 1
        assert result[0]["type"] == "duplicate_event_ids"
        assert result[0]["count"] == 2
        assert len(result[0]["details"]) == 2

    @pytest.mark.asyncio
    async def test_detect_anomalies_high_frequency(
        self, reconciliation_job, mock_session
    ):
        """Test _detect_anomalies method with high frequency events."""
        # Mock no duplicates
        duplicate_result = Mock()
        duplicate_result.fetchall.return_value = []

        # Mock high frequency event types
        reconciliation_job._get_events_by_type = AsyncMock(
            return_value={"payment.completed": 1500, "payment.failed": 50}
        )

        mock_session.execute.return_value = duplicate_result

        start_time = datetime.now(UTC) - timedelta(hours=24)
        end_time = datetime.now(UTC)

        result = await reconciliation_job._detect_anomalies(
            mock_session, start_time, end_time
        )

        assert len(result) == 1
        assert result[0]["type"] == "high_frequency_event"
        assert result[0]["event_type"] == "payment.completed"
        assert result[0]["count"] == 1500

    @pytest.mark.asyncio
    async def test_detect_anomalies_no_anomalies(
        self, reconciliation_job, mock_session
    ):
        """Test _detect_anomalies method with no anomalies."""
        # Mock no duplicates
        duplicate_result = Mock()
        duplicate_result.fetchall.return_value = []

        # Mock normal event frequencies
        reconciliation_job._get_events_by_type = AsyncMock(
            return_value={"payment.completed": 100, "payment.failed": 5}
        )

        mock_session.execute.return_value = duplicate_result

        start_time = datetime.now(UTC) - timedelta(hours=24)
        end_time = datetime.now(UTC)

        result = await reconciliation_job._detect_anomalies(
            mock_session, start_time, end_time
        )

        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_log_reconciliation(self, reconciliation_job, mock_session):
        """Test _log_reconciliation method."""
        summary = {
            "total_events": 15,
            "events_by_provider": {"stripe": 10, "paypal": 5},
            "generated_at": datetime.now(UTC),
        }

        await reconciliation_job._log_reconciliation(mock_session, summary)

        # Verify log entry was added
        mock_session.add.assert_called_once()
        added_log = mock_session.add.call_args[0][0]
        assert isinstance(added_log, ReconciliationLog)
        assert added_log.provider is None
        assert added_log.event_id is None
        assert added_log.status == "completed"
        assert json.loads(added_log.details_json) is not None

        # Verify commit was called
        mock_session.commit.assert_called_once()

    def test_reconciliation_job_initialization(self, reconciliation_job):
        """Test ReconciliationJob initialization."""
        assert reconciliation_job.settings is not None

    def test_global_reconciliation_job_instance(self):
        """Test that global reconciliation_job instance exists."""
        from app.jobs.reconciliation import reconciliation_job

        assert reconciliation_job is not None
        assert isinstance(reconciliation_job, ReconciliationJob)
