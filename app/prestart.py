import logging

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from sqlalchemy import select, Engine
from sqlalchemy.orm import Session
from models import engine

from redis import Redis
from redis_db import redis_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init_db(db_engine: Engine) -> None:
    try:
        with Session(db_engine) as session:
            session.execute(select(1))
            session.commit()
    except Exception as e:
        logger.error(e)
        raise e


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init_redis(client: Redis) -> None:
    try:
        client.ping()
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Inicializando Bases de datos\n")

    logger.info("Base de datos en Postgres")
    init_db(engine)
    print()
    logger.info("Base de datos en Redis")
    init_redis(redis_client)

    print()
    logger.info("Bases de datos inicializadas")
