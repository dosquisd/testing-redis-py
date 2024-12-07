from sqlalchemy import (
    create_engine,
    Column,String,
    Integer,
    ForeignKey
)
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

from config import settings


engine = create_engine(str(settings.POSTGRES_URI))
SessionLocal = sessionmaker(autoflush=True, bind=engine)

BaseModel = declarative_base()


class Authors(BaseModel):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    nacionality = Column(String, nullable=False)

    books = relationship(
        "Books",
        uselist=True,
        back_populates="authors",
        passive_deletes=True,
        passive_updates=True
    )


class Books(BaseModel):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    id_author = Column(Integer, ForeignKey("authors.id"), nullable=False)

    authors = relationship(
        "Authors",
        uselist=True,
        back_populates="books",
        passive_deletes=True,
        passive_updates=True
    )
