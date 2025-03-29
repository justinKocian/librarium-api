from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.book import Book
from app.models.tag import Tag
from app.schemas.book import BookCreate, BookUpdate, BookOut
from app.dependencies.auth import get_current_user, get_current_admin
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=list[BookOut])
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
    book = Book(**data.dict(exclude={"tag_ids"}))
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

    for field, value in data.dict(exclude_unset=True, exclude={"tag_ids"}).items():
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
