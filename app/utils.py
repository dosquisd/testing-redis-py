from sqlalchemy.orm import Session

from models import Authors, Books


def get_author_in(id_author: int, db: Session) -> Authors | None:
    return (
        db.query(Authors)
        .filter(Authors.id == id_author)
        .first()
    )


def get_book_in(id_book: int, db: Session) -> Books | None:
    return (
        db.query(Books)
        .filter(Books.id == id_book)
        .first()
    )
