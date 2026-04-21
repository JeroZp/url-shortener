import redis

from app.config import settings

redis_client: redis.Redis = redis.from_url(settings.redis_url, decode_responses=True)


def check_redis() -> bool:
    """Health check to /ready."""
    try:
        return redis_client.ping()
    except Exception:
        return False
