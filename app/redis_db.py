from redis import Redis
from config import settings
from typing import Any


redis_client: Redis = Redis.from_url(str(settings.REDIS_URI), decode_responses=True)

def set(key: str, value: Any, seconds: int = 0) -> None:
    if seconds <= 0:
        seconds = settings.REDIS_EXPIRE_SECONDS

    redis_client.set(key, value, ex=seconds)


def get(key: str) -> list[str]:
    return redis_client.get(key)


def delete(*keys: str) -> int:
    return redis_client.delete(*keys)


def get_cache() -> dict[str, str]:
    keys = redis_client.keys("*")
    values = redis_client.mget(keys)

    return dict(zip(keys, values))


def clear_cache() -> int:
    keys = redis_client.keys("*")
    return delete(*keys) if len(keys) else 0
