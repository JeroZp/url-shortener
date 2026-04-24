"""
Post-deploy smoke tests.

Explicit ordering (via alphabetical name) so the flow is easy to read:
  1. Health (liveness)
  2. Ready (readiness — DB + Redis connected)
  3. Shorten (POST)
  4. Redirect (GET /s/{code})
  5. Stats (GET /api/stats/{code})
  6. Frontend loads

If any of these fails, the pipeline rolls back to the previous deployment.
"""
from __future__ import annotations

import httpx


def test_01_health(client: httpx.Client) -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json().get("status") == "ok"


def test_02_ready(client: httpx.Client) -> None:
    resp = client.get("/ready")
    assert resp.status_code == 200, f"/ready returned {resp.status_code}: {resp.text}"

    data = resp.json()
    assert data["status"] == "ready"
    assert data["checks"]["db"] is True, "Postgres not reachable from backend"
    assert data["checks"]["redis"] is True, "Redis not reachable from backend"


def test_03_shorten_returns_201(short_code: str) -> None:
    assert len(short_code) == 6


def test_04_redirect_to_original(client: httpx.Client, short_code: str, sample_url: str) -> None:
    resp = client.get(f"/s/{short_code}")

    assert resp.status_code == 301, (
        f"Expected 301 redirect, got {resp.status_code}. "
        "Check that the ALB listener rule routes /s/* to the backend target group."
    )
    assert resp.headers["location"] == sample_url


def test_05_stats_increments(client: httpx.Client, short_code: str, sample_url: str) -> None:
    client.get(f"/s/{short_code}")
    client.get(f"/s/{short_code}")

    resp = client.get(f"/api/stats/{short_code}")
    assert resp.status_code == 200

    data = resp.json()
    assert data["original_url"] == sample_url
    assert data["total_clicks"] >= 2, f"Expected >=2 clicks, got {data['total_clicks']}"
    assert data["last_click_at"] is not None


def test_06_frontend_loads(client: httpx.Client) -> None:
    resp = client.get("/")
    assert resp.status_code == 200
    content_type = resp.headers.get("content-type", "")
    assert "text/html" in content_type, f"Unexpected content-type: {content_type}"
    assert "<html" in resp.text.lower(), "Response body does not look like HTML"
