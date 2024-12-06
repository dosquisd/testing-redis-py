# from redis_om import HashModel
# from typing import Optional


# class Requests(HashModel):
#     endpoint: str
#     method: str
#     body: Optional[dict[str, str]]
#     header: Optional[dict[str, str]]


from redis import Redis
from config import settings
from typing import Any


# redis_client: Redis = Redis(
#     host=settings.REDIS_SERVER,
#     port=settings.REDIS_PORT,
#     username=settings.REDIS_USER,
#     password=settings.REDIS_PASSWORD,
#     decode_responses=True
# )

print(str(settings.REDIS_URI))
redis_client: Redis = Redis.from_url(str(settings.REDIS_URI), decode_responses=True)

def set(key: str, value: Any, seconds: int = 0) -> None:
    if seconds <= 0:
        seconds = settings.REDIS_EXPIRE_SECONDS

    redis_client.set(key, value, ex=seconds)


def get(key: str) -> Any:
    return redis_client.get(key)


def delete(key: str) -> None:
    redis_client.delete(key)


def get_cache() -> dict[str, str]:
    keys = redis_client.keys("*")
    values = redis_client.mget(keys)

    return dict(zip(keys, values))
