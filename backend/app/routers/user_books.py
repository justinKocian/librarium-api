#routers/user_books

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_books import UserBooks, ReadStatus  # ✅ FIXED: plural name
from app.schemas.user_books import UserBookCreate, UserBookUpdate, UserBookOut
from app.models.user import User
from app.dependencies.auth import get_current_user  # ✅ Correct location for auth dependencies

router = APIRouter()

@router.post("/", response_model=UserBookOut)
def create_user_book(
    payload: UserBookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = db.query(UserBooks).filter_by(user_id=current_user.id, book_id=payload.book_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Status already exists for this book")

    user_book = UserBooks(
        user_id=current_user.id,
        book_id=payload.book_id,
        read_status=payload.read_status
    )
    db.add(user_book)
    db.commit()
    db.refresh(user_book)
    return user_book

@router.put("/{book_id}", response_model=UserBookOut)
def update_user_book(
    book_id: int,
    payload: UserBookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_book = db.query(UserBooks).filter_by(user_id=current_user.id, book_id=book_id).first()
    if not user_book:
        raise HTTPException(status_code=404, detail="Status not found")

    user_book.read_status = payload.read_status
    db.commit()
    db.refresh(user_book)
    return user_book

@router.get("/", response_model=list[UserBookOut])
def get_all_user_books(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(UserBooks).filter_by(user_id=current_user.id).all()

@router.get("/{book_id}", response_model=UserBookOut)
def get_user_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_book = db.query(UserBooks).filter_by(user_id=current_user.id, book_id=book_id).first()
    if not user_book:
        raise HTTPException(status_code=404, detail="Status not found")
    return user_book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_book = db.query(UserBooks).filter_by(user_id=current_user.id, book_id=book_id).first()
    if not user_book:
        raise HTTPException(status_code=404, detail="Status not found")

    db.delete(user_book)
    db.commit()
