from sqlalchemy import select, Engine
from sqlalchemy.orm import Session

from models import engine

def init_db(db_engine: Engine) -> None:
    try:
        with Session(db_engine) as session:
            session.execute(select(1))
            session.commit()
    except Exception as e:
        raise e


def main() -> None:
    init_db(engine)


if __name__ == "__main__":
    main()
