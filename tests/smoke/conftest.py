"""
Smoke tests configuration.

These tests run after a deploy against the public ALB DNS of the target
environment (staging or production). They verify that critical endpoints
respond correctly.

Environment variables:
  BASE_URL         Base URL of the environment (e.g. http://my-alb-123.us-east-1.elb.amazonaws.com)
  SMOKE_TIMEOUT    Per-request timeout in seconds (default: 10)
  SMOKE_BOOT_WAIT  Initial wait attempts over /health (default: 30 attempts x 5s)
"""
from __future__ import annotations

import os
import uuid

import httpx
import pytest
from tenacity import retry, stop_after_attempt, wait_fixed


def _base_url() -> str:
    url = os.environ.get("BASE_URL", "").strip()
    if not url:
        pytest.exit("BASE_URL environment variable is required for smoke tests", returncode=2)
    return url.rstrip("/")


@pytest.fixture(scope="session")
def base_url() -> str:
    return _base_url()


@pytest.fixture(scope="session")
def client(base_url: str):
    """HTTP client configured with BASE_URL + active wait on /health."""
    timeout = float(os.environ.get("SMOKE_TIMEOUT", "10"))
    boot_attempts = int(os.environ.get("SMOKE_BOOT_WAIT", "30"))

    with httpx.Client(base_url=base_url, timeout=timeout, follow_redirects=False) as c:

        @retry(stop=stop_after_attempt(boot_attempts), wait=wait_fixed(5), reraise=True)
        def wait_for_boot() -> None:
            resp = c.get("/health")
            if resp.status_code != 200:
                raise AssertionError(f"/health returned {resp.status_code}")

        wait_for_boot()
        yield c


@pytest.fixture(scope="session")
def sample_url() -> str:
    """Unique URL per run to avoid stats pollution across executions."""
    return f"https://example.com/smoke-{uuid.uuid4().hex[:10]}"


@pytest.fixture(scope="session")
def short_code(client: httpx.Client, sample_url: str) -> str:
    """Creates a short code to be reused across several tests."""
    resp = client.post("/api/shorten", json={"url": sample_url})
    assert resp.status_code == 201, f"Shorten failed: {resp.status_code} {resp.text}"
    return resp.json()["short_code"]
