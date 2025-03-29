from pydantic import BaseModel
from typing import Optional, List

class BookBase(BaseModel):
    title: str
    author: str
    isbn: Optional[str] = None
    genre_id: Optional[int] = None
    series_id: Optional[int] = None
    volume: Optional[int] = None
    tag_ids: Optional[List[int]] = []

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class BookOut(BookBase):
    id: int
    cover_path: Optional[str]

    class Config:
        from_attributes = True
