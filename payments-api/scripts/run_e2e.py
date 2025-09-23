#!/usr/bin/env python3
"""Script to run E2E tests with a temporary server."""

import asyncio
import subprocess
import sys
import time

import httpx

from app.utils.ports import get_app_port


async def run_e2e():
    """Run E2E tests with temporary server."""
    port = 8065  # Use fixed port for E2E tests
    print(f"Starting server on port {port}")

    # Start server
    proc = subprocess.Popen([
        "uvicorn", "app.main:app",
        "--host", "0.0.0.0",
        "--port", str(port)
    ])

    # Wait for server to be ready with retry logic
    max_retries = 10
    retry_delay = 1

    try:
        for attempt in range(max_retries):
            await asyncio.sleep(retry_delay)
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"http://127.0.0.1:{port}/health")
                    if response.status_code == 200:
                        print("Server ready, running E2E tests...")
                        result = subprocess.run([
                            "pytest", "tests/e2e/", "-v", "--tb=short"
                        ])
                        sys.exit(result.returncode)
            except (httpx.ConnectError, httpx.RequestError):
                print(f"Attempt {attempt + 1}/{max_retries}: Server not ready yet...")
                if attempt == max_retries - 1:
                    print("Server failed to start")
                    sys.exit(1)
    finally:
        proc.terminate()
        proc.wait()


if __name__ == "__main__":
    asyncio.run(run_e2e())