import fakeredis
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import cache
from app.db import get_db
from app.main import app
from app.models import Base


@pytest.fixture
def sample_url() -> str:
    return "https://example.com/some/long/path"


@pytest.fixture
def test_db(monkeypatch):
    """DB SQLite in-memory, aislada por test."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    # Override get_db to use the test session
    from app import db as db_module

    monkeypatch.setattr(db_module, "engine", engine)
    monkeypatch.setattr(db_module, "SessionLocal", TestSession)

    def override_get_db():
        session = TestSession()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestSession
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def fake_redis(monkeypatch):
    """Fake redis isolated for test."""
    fake = fakeredis.FakeRedis(decode_responses=True)
    monkeypatch.setattr(cache, "redis_client", fake)
    import app.main

    monkeypatch.setattr(app.main, "redis_client", fake)
    yield fake


@pytest.fixture
def client(test_db, fake_redis):
    """HTTP client test with DB and Redis isolated."""
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def override_health_checks(monkeypatch):
    """En tests, los health checks siempre retornan True."""
    from app import db as db_module

    monkeypatch.setattr(db_module, "check_db", lambda: True)
    import app.main

    monkeypatch.setattr(app.main, "check_db", lambda: True)
    monkeypatch.setattr(app.main, "check_redis", lambda: True)
