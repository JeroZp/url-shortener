import pytest


@pytest.fixture
def sample_url() -> str:
    return "https://www.example.com/some/long/path"