from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from app.models.book import Book
from app.models.tag import Tag

def search_books(
    db: Session,
    q: Optional[str] = None,
    genre_id: Optional[int] = None,
    tag_ids: Optional[List[int]] = None,
    series_id: Optional[int] = None,
    volume: Optional[int] = None,
    read_status: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
) -> List[Book]:
    query = db.query(Book)

    if q:
        query = query.filter(
            or_(
                Book.title.ilike(f"%{q}%"),
                Book.author.ilike(f"%{q}%"),
                Book.isbn.ilike(f"%{q}%")
            )
        )

    if genre_id:
        query = query.filter(Book.genre_id == genre_id)

    if tag_ids:
        query = query.join(Book.tags).filter(Tag.id.in_(tag_ids))

    if series_id:
        query = query.filter(Book.series_id == series_id)

    if volume:
        query = query.filter(Book.volume == volume)

    if read_status:
        query = query.filter(Book.read_status == read_status)

    return query.offset(offset).limit(limit).all()
