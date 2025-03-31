from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from app.models.book import Book
from app.models.tag import Tag

from app.utils.pagination import paginate_query

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
    sort_by: Optional[str] = "title",
    sort_order: Optional[str] = "asc",
) -> Tuple[int, List[Book]]:
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

    return paginate_query(query, Book, limit, offset, sort_by, sort_order)