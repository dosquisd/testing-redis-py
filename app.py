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

import redis_db
from sqlalchemy.orm import Session

import json

from prestart import main

from collections.abc import Generator
from typing import Annotated


def get_url() -> Generator[Session, None, None]:
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def lifespan(app: FastAPI):
    main()
    yield


app = FastAPI(lifespan=lifespan)

SessionDep = Annotated[Session, Depends(get_url)]


# ----------------------------- GET -----------------------------
@app.get("/", status_code=200)
async def root() -> ApiResponseDefault:
    return {"detail": "HOLI"}


@app.get("/books", status_code=200)
async def get_books(db: SessionDep) -> list[Books]:
    cache_key = "get_books"
    cached_books = redis_db.get(cache_key)

    if cached_books:
        return json.loads(cached_books)

    books = list(
        map(
            lambda obj: Books.model_validate(obj),
            db.query(models.Books).all())
    )

    redis_db.set(cache_key, json.dumps([book.model_dump() for book in books]))
    return books


@app.get("/authors", status_code=200)
async def get_authors(db: SessionDep) -> list[Authors]:
    cache_key = "get_authors"
    cached_books = redis_db.get(cache_key)

    if cached_books:
        return json.loads(cached_books)

    authors = list(
        map(
            lambda obj: Authors.model_validate(obj), 
            db.query(models.Authors).all()
        )
    )

    redis_db.set(cache_key, json.dumps(author.model_dump() for author in authors))
    return authors


@app.get("/books/{id_book}", status_code=200)
async def get_book(id_book: int, db: SessionDep) -> Books:
    cache_key = f"get_books_{id_book}"
    cached_book = redis_db.get(cache_key)

    if cached_book:
        return json.loads(cached_book)

    try:
        book = Books.model_validate(
            db.query(models.Books)
            .filter(models.Books.id == id_book)
            .first()
        )
    except Exception as e:
        raise HTTPException(404, detail=repr(e))

    redis_db.set(cache_key, json.dumps(book))
    return book


@app.get("/authors/{id_author}", status_code=200)
async def get_author(id_author: int, db: SessionDep) -> Authors:
    cache_key = f"get_authors_{id_author}"
    cached_author = redis_db.get(cache_key)

    if cached_author:
        return json.loads(cached_author)

    try:
        author = Authors.model_validate(
            db.query(models.Authors)
            .filter(models.Authors.id == id_author)
            .first()
        )
    except Exception as e:
        raise HTTPException(404, detail=repr(e))

    redis_db.set(cache_key, json.dumps(author))
    return author


@app.get("/cache")
async def get_cache():
    cache_key = "get_cache"
    cached_value = redis_db.get(cache_key)

    if cached_value:
        return json.loads(cached_value)

    cache = redis_db.get_cache()

    redis_db.set(cache_key, json.dumps(cache))
    return cache


# ----------------------------- POST -----------------------------
@app.post("/authors", status_code=201)
async def add_author(db: SessionDep, author: CreateAuthor) -> Authors:
    db_author = models.Authors(
        name=author.name,
        nacionality=author.nacionality
    )

    db.add(db_author)
    db.commit()

    redis_db.delete("get_authors")
    return Authors.model_validate(db_author)


@app.post("/books", status_code=201)
async def add_book(db: SessionDep, book: CreateBook) -> Books:
    db_book = models.Books(
        title=book.title,
        genre=book.genre,
        id_author=book.id_author
    )

    db.add(db_book)
    db.commit()

    redis_db.delete("get_books")
    return Books.model_validate(db_book)


# ----------------------------- PUT -----------------------------
@app.put("/books/{id_book}", status_code=200)
async def update_book(id_book: str, db: SessionDep, book: UpdateBook) -> Books:
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

    redis_db.delete(f"get_books_{id_book}")
    return Books.model_validate(book_in)


@app.put("/authors/{id_author}", status_code=200)
async def update_author(id_author: str, db: SessionDep, author: UpdateAuthor) -> Books:
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

    redis_db.delete(f"get_authors_{id_author}")
    return Authors.model_validate(author_in)


# ----------------------------- DELETE -----------------------------
@app.delete("/books/{id_book}", status_code=200)
async def delete_book(id_book: int, db: SessionDep) -> Books:
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

    redis_db.delete(f"get_books")
    redis_db.delete(f"get_books_{id_book}")
    return Books.model_validate(book_in)


@app.delete("/authors/{id_author}", status_code=200)
async def delete_author(id_author: int, db: SessionDep) -> Authors:
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

    redis_db.delete(f"get_authors")
    redis_db.delete(f"get_authors_{id_author}")
    return Authors.model_validate(author_in)


@app.delete("/cache")
async def clear_cache():
    keys = redis_db.redis_client.keys("*")
    return redis_db.delete(*keys)
