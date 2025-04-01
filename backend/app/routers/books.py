from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.tag import Tag
from app.models.user import User
from app.schemas.book import BookCreate, BookUpdate, BookOut
from app.schemas.pagination import PaginatedResponse
from app.utils.pagination import paginate_query
from app.dependencies.auth import get_current_user, get_current_admin
from app.database import get_db
from app.services import book as book_service
from app.core.exceptions import NotFoundException

router = APIRouter()

@router.get(
    "/search",
    response_model=PaginatedResponse[BookOut],
    summary="Search books",
    description=(
        "Search for books using full-text matching across title, author, or ISBN. "
        "You can also filter by genre, tags, series, volume, and reading status. "
        "Results are paginated and support sorting."
    )
)
def search_books(
    q: Optional[str] = None,
    genre_id: Optional[int] = None,
    tag_ids: Optional[List[int]] = Query(default=None),
    series_id: Optional[int] = None,
    volume: Optional[int] = None,
    read_status: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    sort_by: str = "title",
    sort_order: str = "asc",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total, books = book_service.search_books(
        db=db,
        q=q,
        genre_id=genre_id,
        tag_ids=tag_ids,
        series_id=series_id,
        volume=volume,
        read_status=read_status,
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return {"total": total, "items": books}

@router.get(
    "/",
    response_model=PaginatedResponse[BookOut],
    summary="List all books",
    description=(
        "Retrieve a paginated list of all books in the library. "
        "Supports sorting by any sortable field such as title or author."
    )
)
def get_books(
    db: Session = Depends(get_db),
    limit: int = 20,
    offset: int = 0,
    sort_by: Optional[str] = "title",
    sort_order: Optional[str] = "asc"
):
    query = db.query(Book)
    total, items = paginate_query(query, Book, limit, offset, sort_by, sort_order)
    return {"total": total, "items": items}

@router.get(
    "/{book_id}",
    response_model=BookOut,
    summary="Get a book by ID",
    description="Retrieve detailed information for a specific book using its ID."
)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise NotFoundException("Book not found")
    return book

@router.post(
    "/",
    response_model=BookOut,
    summary="Create a new book",
    description=(
        "Add a new book to the library. Admin only. "
        "Optionally include tag IDs for assignment during creation."
    )
)
def create_book(data: BookCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    book = Book(**data.model_dump(exclude={"tag_ids"}))
    if data.tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(data.tag_ids)).all()
        book.tags = tags
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

@router.put(
    "/{book_id}",
    response_model=BookOut,
    summary="Update a book",
    description=(
        "Update fields on an existing book by ID. Admin only. "
        "To change tags, supply a new list of tag IDs."
    )
)
def update_book(book_id: int, data: BookUpdate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise NotFoundException("Book not found")

    for field, value in data.model_dump(exclude_unset=True, exclude={"tag_ids"}).items():
        setattr(book, field, value)

    if data.tag_ids is not None:
        book.tags = db.query(Tag).filter(Tag.id.in_(data.tag_ids)).all()

    db.commit()
    db.refresh(book)
    return book

@router.delete(
    "/{book_id}",
    summary="Delete a book",
    description="Delete a book from the library by ID. Admin only."
)
def delete_book(book_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise NotFoundException("Book not found")
    db.delete(book)
    db.commit()
    return {"detail": "Book deleted"}
