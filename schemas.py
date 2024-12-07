from pydantic import BaseModel
from typing import TypedDict, Optional


class CreateBook(BaseModel):
    title: str
    genre: str
    id_author: int


class CreateAuthor(BaseModel):
    name: str
    nacionality: str


class Authors(BaseModel):
    id: int
    name: str
    nacionality: str

    class Config:
        from_attributes = True


class Books(BaseModel):
    id: int
    title: str
    genre: str
    id_author: int

    class Config:
        from_attributes = True


class UpdateBook(BaseModel):
    title: Optional[str]
    genre: Optional[str]
    id_author: Optional[int]


class UpdateAuthor(BaseModel):
    name: Optional[str]
    nacionality: Optional[str]
