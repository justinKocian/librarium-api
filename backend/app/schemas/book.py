# app/schemas/book.py

from pydantic import BaseModel
from typing import Optional, List
from app.schemas.genre import GenreRead
from app.schemas.tag import TagRead
from app.schemas.series import SeriesRead


class BookBase(BaseModel):
    title: str
    author: str
    isbn: Optional[str] = None
    volume: Optional[int] = None
    cover_path: Optional[str] = None
    read_status: Optional[str] = None


class BookCreate(BookBase):
    genre_id: int
    series_id: Optional[int] = None
    tag_ids: Optional[List[int]] = []


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    volume: Optional[int] = None
    cover_path: Optional[str] = None
    read_status: Optional[str] = None
    genre_id: Optional[int] = None
    series_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None


class BookOut(BookBase):
    id: int
    genre: GenreRead
    tags: List[TagRead]
    series: Optional[SeriesRead] = None

    class Config:
        from_attributes = True
