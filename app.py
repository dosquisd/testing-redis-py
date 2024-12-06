from fastapi import FastAPI, Depends, HTTPException

import models
from schemas import (
    ApiResponseDefault,
    CreateBook,
    CreateAuthor,
    Authors,
    Books,
    UpdateBook,
    UpdateAuthor
)

from collections.abc import Generator
from typing import Annotated

from sqlalchemy.orm import Session


def get_url() -> Generator[Session, None, None]:
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

SessionDep = Annotated[Session, Depends(get_url)]


@app.get("/", status_code=200)
def root() -> ApiResponseDefault:
    return {"detail": "HOLI"}


# ----------------------------- GET -----------------------------
@app.get("/books", status_code=200)
def get_books(db: SessionDep) -> list[Books]:
    return list(
        map(
            lambda obj: Books.model_validate(obj),
            db.query(models.Books).all())
    )


@app.get("/authors", status_code=200)
def get_authors(db: SessionDep) -> list[Authors]:
    return list(
        map(
            lambda obj: Authors.model_validate(obj), 
            db.query(models.Authors).all()
        )
    )


@app.get("/books/{id_book}", status_code=200)
def get_book(id_book: int, db: SessionDep) -> Books:
    try:
        return Books.model_validate(
            db.query(models.Books)
            .filter(models.Books.id == id_book)
            .first()
        )
    except Exception as e:
        raise HTTPException(404, detail=repr(e))


@app.get("/authors/{id_author}", status_code=200)
def get_author(id_author: int, db: SessionDep) -> Authors:
    try:
        return Authors.model_validate(
            db.query(models.Authors)
            .filter(models.Authors.id == id_author)
            .first()
        )
    except Exception as e:
        raise HTTPException(404, detail=repr(e))


# ----------------------------- POST -----------------------------
@app.post("/authors", status_code=201)
def add_author(db: SessionDep, author: CreateAuthor) -> Authors:
    db_author = models.Authors(
        name=author.name,
        nacionality=author.nacionality
    )

    db.add(db_author)
    db.commit()

    return Authors.model_validate(db_author)


@app.post("/books", status_code=201)
def add_author(db: SessionDep, book: CreateBook) -> Books:
    db_book = models.Books(
        title=book.title,
        genre=book.genre,
        id_author=book.id_author
    )

    db.add(db_book)
    db.commit()

    return Books.model_validate(db_book)


# ----------------------------- PUT -----------------------------
@app.put("/books/{id_book}", status_code=200)
def update_book(id_book: str, db: SessionDep, book: UpdateBook) -> Books:
    try:
        book_in = (
            db.query(models.Books)
            .filter(models.Books.id == id_book)
            .first()
        )
    except Exception as e:
        raise HTTPException(404, detail=repr(e))

    if book.title is not None:
        book_in.title = book.title

    if book.genre is not None:
        book_in.genre = book.genre

    if book.id_author is not None:
        book_in.id_author = book.id_author

    db.commit()
    db.refresh(book_in)

    return Books.model_validate(book_in)


@app.put("/authors/{id_author}", status_code=200)
def update_author(id_author: str, db: SessionDep, author: UpdateAuthor) -> Books:
    try:
        author_in = (
            db.query(models.Authors)
            .filter(models.Authors.id == id_author)
            .first()
        )
    except Exception as e:
        raise HTTPException(404, detail=repr(e))

    if author.name is not None:
        author_in.name = author.name

    if author.nacionality is not None:
        author_in.nacionality = author.nacionality

    db.commit()
    db.refresh(author_in)

    return Authors.model_validate(author_in)


# ----------------------------- DELETE -----------------------------
@app.delete("/books/{id_book}", status_code=200)
def delete_book(id_book: int, db: SessionDep) -> Books:
    try:
        book_in = (
            db.query(models.Books)
            .filter(models.Books.id == id_book)
            .first()
        )
    except Exception as e:
        raise HTTPException(404, detail=repr(e))

    db.delete(book_in)
    db.commit()
    
    return Books.model_validate(book_in)


@app.delete("/authors/{id_author}", status_code=200)
def delete_author(id_author: int, db: SessionDep) -> Authors:
    try:
        author_in = (
            db.query(models.Authors)
            .filter(models.Authors.id == id_author)
            .first()
        )
    except Exception as e:
        raise HTTPException(404, detail=repr(e))
    
    db.delete(author_in)
    db.commit()

    return Authors.model_validate(author_in)
