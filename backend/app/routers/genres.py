from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.genre import Genre
from app.schemas.genre import GenreCreate, GenreRead
from app.dependencies.auth import get_current_admin
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=list[GenreRead])
def list_genres(db: Session = Depends(get_db)):
    return db.query(Genre).all()

@router.post("/", response_model=GenreRead)
def create_genre(data: GenreCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    existing = db.query(Genre).filter_by(name=data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Genre already exists")
    genre = Genre(name=data.name)
    db.add(genre)
    db.commit()
    db.refresh(genre)
    return genre
