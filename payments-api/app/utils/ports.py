import socket


def find_free_port(start_port: int = 8065, end_port: int = 8099) -> int | None:
    """
    Find a free port in the specified range by attempting to bind to each port.

    Args:
        start_port: Starting port number (inclusive)
        end_port: Ending port number (inclusive)

    Returns:
        First available port number or None if no ports are available
    """
    # Skip common dev ports that might be in use
    skip_ports = {3000, 5173, 8000, 8080, 9000}

    for port in range(start_port, end_port + 1):
        if port in skip_ports:
            continue

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind(("127.0.0.1", port))
                return port
        except OSError:
            continue

    return None


def get_app_port() -> int:
    """
    Get the application port from environment or find a free one.

    Returns:
        Port number to use for the application

    Raises:
        RuntimeError: If no free ports are available
    """
    import os

    # Check if port is specified in environment
    env_port = os.getenv("APP_PORT")
    if env_port:
        try:
            port = int(env_port)
            # Verify the port is actually available
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind(("127.0.0.1", port))
                return port
        except (ValueError, OSError) as e:
            print(f"Warning: Specified APP_PORT={env_port} is not available: {e}")

    # Find a free port
    port = find_free_port()
    if port is None:
        raise RuntimeError("No free ports available in range [8065-8099]")

    return port
