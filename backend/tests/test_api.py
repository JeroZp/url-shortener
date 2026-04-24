def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ready_endpoint(client):
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["checks"]["db"] is True
    assert data["checks"]["redis"] is True


def test_shorten_url_success(client, sample_url):
    response = client.post("/api/shorten", json={"url": sample_url})
    assert response.status_code == 201
    data = response.json()
    assert "short_code" in data
    assert len(data["short_code"]) == 6
    assert data["original_url"] == sample_url
    assert data["short_url"].endswith(f"/s/{data['short_code']}")


def test_shorten_url_invalid_returns_422(client):
    response = client.post("/api/shorten", json={"url": "not-a-valid-url"})
    assert response.status_code == 422


def test_shorten_url_missing_body_returns_422(client):
    response = client.post("/api/shorten", json={})
    assert response.status_code == 422


def test_redirect_to_original_url(client, sample_url):
    # Create short URL
    create = client.post("/api/shorten", json={"url": sample_url})
    short_code = create.json()["short_code"]

    # Test redirect
    response = client.get(f"/s/{short_code}", follow_redirects=False)
    assert response.status_code == 301
    assert response.headers["location"] == sample_url


def test_redirect_unknown_code_returns_404(client):
    response = client.get("/s/nonexistent", follow_redirects=False)
    assert response.status_code == 404


def test_stats_returns_click_count(client, sample_url):
    # Create short URL
    create = client.post("/api/shorten", json={"url": sample_url})
    short_code = create.json()["short_code"]

    # Make 3 clicks
    for _ in range(3):
        client.get(f"/s/{short_code}", follow_redirects=False)

    # Verify stats
    stats = client.get(f"/api/stats/{short_code}")
    assert stats.status_code == 200
    data = stats.json()
    assert data["total_clicks"] == 3
    assert data["original_url"] == sample_url
    assert data["last_click_at"] is not None


def test_stats_unknown_code_returns_404(client):
    response = client.get("/api/stats/nonexistent")
    assert response.status_code == 404


def test_stats_zero_clicks(client, sample_url):
    create = client.post("/api/shorten", json={"url": sample_url})
    short_code = create.json()["short_code"]

    stats = client.get(f"/api/stats/{short_code}")
    assert stats.json()["total_clicks"] == 0
    assert stats.json()["last_click_at"] is None
