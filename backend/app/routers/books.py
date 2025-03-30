from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.tag import Tag
from app.models.user import User
from app.schemas.book import BookCreate, BookUpdate, BookOut
from app.dependencies.auth import get_current_user, get_current_admin
from app.database import get_db
from app.services import book as book_service

router = APIRouter()

@router.get("/search", response_model=List[BookOut])
def search_books(
    q: Optional[str] = None,
    genre_id: Optional[int] = None,
    tag_ids: Optional[List[int]] = Query(default=None),
    series_id: Optional[int] = None,
    volume: Optional[int] = None,
    read_status: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return book_service.search_books(
        db=db,
        q=q,
        genre_id=genre_id,
        tag_ids=tag_ids,
        series_id=series_id,
        volume=volume,
        read_status=read_status,
        limit=limit,
        offset=offset,
    )

@router.get("/", response_model=List[BookOut])
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=BookOut)
def create_book(data: BookCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    book = Book(**data.model_dump(exclude={"tag_ids"}))
    if data.tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(data.tag_ids)).all()
        book.tags = tags
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

@router.put("/{book_id}", response_model=BookOut)
def update_book(book_id: int, data: BookUpdate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    for field, value in data.model_dump(exclude_unset=True, exclude={"tag_ids"}).items():
        setattr(book, field, value)

    if data.tag_ids is not None:
        book.tags = db.query(Tag).filter(Tag.id.in_(data.tag_ids)).all()

    db.commit()
    db.refresh(book)
    return book

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"detail": "Book deleted"}
