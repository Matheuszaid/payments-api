import socket
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from app.utils.ports import find_free_port
from app.utils.ports import get_app_port


class TestFindFreePort:
    """Test free port finding functionality."""

    def test_find_free_port_success(self):
        """Test finding a free port successfully."""
        port = find_free_port(8065, 8070)
        assert port is not None
        assert 8065 <= port <= 8070

    def test_find_free_port_skip_common_ports(self):
        """Test that common dev ports are skipped."""
        # Mock socket to make all ports appear available
        with patch("socket.socket") as mock_socket:
            mock_socket.return_value.__enter__.return_value.bind.return_value = None

            port = find_free_port(3000, 3000)  # 3000 is a common port
            assert port is None  # Should be skipped

    @patch("socket.socket")
    def test_find_free_port_all_ports_busy(self, mock_socket):
        """Test when all ports are busy."""
        # Make all bind attempts fail
        mock_socket.return_value.__enter__.return_value.bind.side_effect = OSError()

        port = find_free_port(8065, 8067)
        assert port is None

    @patch("socket.socket")
    def test_find_free_port_second_port_available(self, mock_socket):
        """Test when second port in range is available."""
        mock_sock = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_sock

        # First port busy, second port free
        mock_sock.bind.side_effect = [OSError(), None]

        port = find_free_port(8065, 8066)
        assert port == 8066


class TestGetAppPort:
    """Test application port configuration."""

    @patch.dict("os.environ", {"APP_PORT": "8080"})
    def test_get_app_port_from_env(self):
        """Test getting port from environment variable."""
        port = get_app_port()
        assert port == 8080

    @patch.dict("os.environ", {"APP_PORT": "invalid"})
    def test_get_app_port_invalid_env(self):
        """Test handling invalid port in environment."""
        # Should fall back to finding free port
        port = get_app_port()
        assert port is not None
        assert isinstance(port, int)

    @patch.dict("os.environ", {}, clear=True)
    def test_get_app_port_no_env(self):
        """Test getting port when no environment variable set."""
        port = get_app_port()
        assert port is not None
        assert 8065 <= port <= 8099

    @patch.dict("os.environ", {"APP_PORT": "8080"})
    @patch("socket.socket")
    @patch("app.utils.ports.find_free_port")
    def test_get_app_port_env_port_busy(self, mock_find_free_port, mock_socket):
        """Test when environment port is busy."""
        # Make the specified port unavailable
        mock_socket.return_value.__enter__.return_value.bind.side_effect = OSError()
        # Mock find_free_port to return a valid alternative
        mock_find_free_port.return_value = 8067

        port = get_app_port()
        # Should find alternative port
        assert port == 8067
        assert isinstance(port, int)

    @patch("app.utils.ports.find_free_port")
    def test_get_app_port_no_free_ports(self, mock_find_free_port):
        """Test when no free ports are available."""
        mock_find_free_port.return_value = None

        with pytest.raises(RuntimeError, match="No free ports available"):
            get_app_port()

    def test_port_range_constraints(self):
        """Test that port finding respects range constraints."""
        port = find_free_port(8065, 8065)
        assert port is None or port == 8065

    def test_port_actually_available(self):
        """Test that returned port is actually available."""
        port = find_free_port()
        if port is not None:
            # Try to bind to the port to verify it's available
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    sock.bind(("127.0.0.1", port))
                    assert True  # Successfully bound
            except OSError:
                pytest.fail(f"Port {port} reported as free but binding failed")
