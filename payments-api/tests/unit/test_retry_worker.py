import asyncio
from datetime import UTC
from datetime import datetime
from datetime import timedelta
from unittest.mock import AsyncMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest

from app.jobs.retry_worker import RetryWorker
from app.jobs.retry_worker import add_to_dlq
from app.models import DLQMessage


class TestRetryWorker:
    """Test cases for RetryWorker."""

    @pytest.fixture
    def retry_worker(self):
        """Create a RetryWorker instance for testing."""
        return RetryWorker(max_concurrent=3)

    @pytest.fixture
    def mock_session(self):
        """Create a mock database session."""
        session = AsyncMock()
        session.execute = AsyncMock()
        session.add = Mock()
        session.commit = AsyncMock()
        session.rollback = AsyncMock()
        session.delete = AsyncMock()
        session.flush = AsyncMock()
        return session

    @pytest.fixture
    def sample_dlq_message(self):
        """Create a sample DLQ message for testing."""
        return DLQMessage(
            id=1,
            provider="stripe",
            event_id="evt_123",
            payload_json='{"test": "data"}',
            error_kind="timeout",
            attempts=0,
            next_retry_at=datetime.now(UTC),
        )

    def test_retry_worker_initialization(self):
        """Test RetryWorker initialization."""
        worker = RetryWorker(max_concurrent=5)
        assert worker.max_concurrent == 5
        assert worker.running is False
        assert isinstance(worker.semaphore, asyncio.Semaphore)

    def test_retry_worker_default_initialization(self):
        """Test RetryWorker with default parameters."""
        worker = RetryWorker()
        assert worker.max_concurrent == 5

    @pytest.mark.asyncio
    async def test_start_and_stop(self, retry_worker):
        """Test starting and stopping the retry worker."""
        # Mock the _process_due_messages to avoid infinite loop
        retry_worker._process_due_messages = AsyncMock()

        # Start worker in background
        task = asyncio.create_task(retry_worker.start())

        # Give it a moment to start
        await asyncio.sleep(0.1)
        assert retry_worker.running is True

        # Stop the worker
        await retry_worker.stop()
        assert retry_worker.running is False

        # Cancel the task to clean up
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    @pytest.mark.asyncio
    async def test_start_handles_exception(self, retry_worker):
        """Test that start method handles exceptions gracefully."""
        # Mock _process_due_messages to raise exception then succeed
        call_count = 0

        async def side_effect():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise Exception("Test error")
            # Stop after second call to avoid infinite loop
            retry_worker.running = False

        retry_worker._process_due_messages = AsyncMock(side_effect=side_effect)

        # Start worker
        await retry_worker.start()

        # Verify it handled the exception and continued
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_process_due_messages_no_messages(self, retry_worker, mock_session):
        """Test _process_due_messages when no messages are due."""

        # Mock db_manager.get_session() as async generator
        async def mock_get_session():
            yield mock_session

        with patch("app.jobs.retry_worker.db_manager") as mock_db_manager:
            mock_db_manager.get_session = mock_get_session

            # Mock empty result
            mock_result = Mock()
            mock_result.scalars.return_value.all.return_value = []
            mock_session.execute.return_value = mock_result

            await retry_worker._process_due_messages()

            # Verify query was executed
            mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_process_due_messages_with_messages(
        self, retry_worker, mock_session, sample_dlq_message
    ):
        """Test _process_due_messages with messages to process."""

        # Mock db_manager.get_session() as async generator
        async def mock_get_session():
            yield mock_session

        with patch("app.jobs.retry_worker.db_manager") as mock_db_manager:
            mock_db_manager.get_session = mock_get_session

            # Mock result with messages
            mock_result = Mock()
            mock_result.scalars.return_value.all.return_value = [sample_dlq_message]
            mock_session.execute.return_value = mock_result

            # Mock _process_message
            retry_worker._process_message = AsyncMock()

            await retry_worker._process_due_messages()

            # Verify message was processed
            retry_worker._process_message.assert_called_once_with(
                sample_dlq_message, mock_session
            )

    @pytest.mark.asyncio
    async def test_process_due_messages_handles_exception(
        self, retry_worker, mock_session
    ):
        """Test _process_due_messages handles database exceptions."""

        # Mock db_manager.get_session() normally but session.execute() raises exception
        async def mock_get_session():
            yield mock_session

        with patch("app.jobs.retry_worker.db_manager") as mock_db_manager:
            mock_db_manager.get_session = mock_get_session

            # Mock session.execute to raise exception
            mock_session.execute.side_effect = Exception("Database error")

            # Should not raise exception (it should be caught and logged)
            await retry_worker._process_due_messages()

    @pytest.mark.asyncio
    async def test_process_message_success(
        self, retry_worker, mock_session, sample_dlq_message
    ):
        """Test _process_message with successful processing."""
        # Mock successful processing
        retry_worker._simulate_processing = AsyncMock(return_value=True)

        await retry_worker._process_message(sample_dlq_message, mock_session)

        # Verify message was deleted
        mock_session.delete.assert_called_once_with(sample_dlq_message)
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_process_message_failure(
        self, retry_worker, mock_session, sample_dlq_message
    ):
        """Test _process_message with failed processing."""
        # Mock failed processing
        retry_worker._simulate_processing = AsyncMock(return_value=False)
        initial_attempts = sample_dlq_message.attempts

        await retry_worker._process_message(sample_dlq_message, mock_session)

        # Verify retry info was updated
        assert sample_dlq_message.attempts == initial_attempts + 1
        assert sample_dlq_message.next_retry_at > datetime.now(UTC)
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_process_message_exception(
        self, retry_worker, mock_session, sample_dlq_message
    ):
        """Test _process_message handles processing exceptions."""
        # Mock processing to raise exception
        retry_worker._simulate_processing = AsyncMock(
            side_effect=Exception("Processing error")
        )

        await retry_worker._process_message(sample_dlq_message, mock_session)

        # Verify rollback was called
        mock_session.rollback.assert_called_once()

    @pytest.mark.asyncio
    async def test_simulate_processing(self, retry_worker, sample_dlq_message):
        """Test _simulate_processing method."""
        # Mock random to return predictable result
        with patch("app.jobs.retry_worker.random.random", return_value=0.5):
            result = await retry_worker._simulate_processing(sample_dlq_message)
            assert result is True  # 0.5 < 0.7

        with patch("app.jobs.retry_worker.random.random", return_value=0.8):
            result = await retry_worker._simulate_processing(sample_dlq_message)
            assert result is False  # 0.8 >= 0.7

    def test_calculate_next_retry(self, retry_worker):
        """Test _calculate_next_retry method."""
        now = datetime.now(UTC)

        # Test first attempt (2^1 = 2 minutes base)
        with patch("app.jobs.retry_worker.random.random", return_value=0.5):
            next_retry = retry_worker._calculate_next_retry(1)
            expected_base = 2 * 60  # 2 minutes in seconds
            expected_min = now + timedelta(seconds=expected_base * 0.75)
            expected_max = now + timedelta(seconds=expected_base * 1.25)
            assert expected_min <= next_retry <= expected_max

        # Test high attempt (should be capped at 60 minutes)
        with patch("app.jobs.retry_worker.random.random", return_value=0.5):
            next_retry = retry_worker._calculate_next_retry(10)
            expected_base = 60 * 60  # 60 minutes in seconds (capped)
            expected_min = now + timedelta(seconds=expected_base * 0.75)
            expected_max = now + timedelta(seconds=expected_base * 1.25)
            assert expected_min <= next_retry <= expected_max

    def test_calculate_next_retry_jitter_bounds(self, retry_worker):
        """Test that jitter stays within bounds."""
        # Test with minimum jitter
        with patch("app.jobs.retry_worker.random.random", return_value=0.0):
            next_retry = retry_worker._calculate_next_retry(1)
            # Should be base_delay - 25%
            base_delay = 2 * 60  # 2 minutes
            min_delay = base_delay * 0.75
            expected = datetime.now(UTC) + timedelta(seconds=min_delay)
            # Allow small tolerance for execution time
            assert abs((next_retry - expected).total_seconds()) < 1

        # Test with maximum jitter
        with patch("app.jobs.retry_worker.random.random", return_value=1.0):
            next_retry = retry_worker._calculate_next_retry(1)
            # Should be base_delay + 25%
            base_delay = 2 * 60  # 2 minutes
            max_delay = base_delay * 1.25
            expected = datetime.now(UTC) + timedelta(seconds=max_delay)
            # Allow small tolerance for execution time
            assert abs((next_retry - expected).total_seconds()) < 1


class TestAddToDLQ:
    """Test cases for add_to_dlq function."""

    @pytest.fixture
    def mock_session(self):
        """Create a mock database session."""
        session = AsyncMock()
        session.add = Mock()
        session.flush = AsyncMock()
        return session

    @pytest.mark.asyncio
    async def test_add_to_dlq_success(self, mock_session):
        """Test successful addition to DLQ."""
        provider = "stripe"
        event_id = "evt_123"
        payload_json = '{"test": "data"}'
        error_kind = "timeout"

        result = await add_to_dlq(
            mock_session, provider, event_id, payload_json, error_kind
        )

        # Verify DLQMessage was created correctly
        assert isinstance(result, DLQMessage)
        assert result.provider == provider
        assert result.event_id == event_id
        assert result.payload_json == payload_json
        assert result.error_kind == error_kind
        assert result.attempts == 0
        assert result.next_retry_at > datetime.now(UTC)

        # Verify session operations
        mock_session.add.assert_called_once_with(result)
        mock_session.flush.assert_called_once()

    @pytest.mark.asyncio
    async def test_add_to_dlq_timing(self, mock_session):
        """Test that next_retry_at is set correctly."""
        before_time = datetime.now(UTC)

        result = await add_to_dlq(
            mock_session, "paypal", "evt_456", "{}", "validation_error"
        )

        after_time = datetime.now(UTC) + timedelta(minutes=2)

        # Should be approximately 1 minute from now
        expected_time = before_time + timedelta(minutes=1)
        assert before_time < result.next_retry_at < after_time
        assert abs((result.next_retry_at - expected_time).total_seconds()) < 60


def test_global_retry_worker_instance():
    """Test that global retry_worker instance exists."""
    from app.jobs.retry_worker import retry_worker

    assert retry_worker is not None
    assert isinstance(retry_worker, RetryWorker)
    assert retry_worker.max_concurrent == 5
