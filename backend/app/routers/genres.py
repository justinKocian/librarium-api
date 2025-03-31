from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.genre import Genre
from app.schemas.genre import GenreCreate, GenreRead
from app.dependencies.auth import get_current_admin
from app.database import get_db
from app.core.exceptions import AlreadyExistsException
from app.utils.pagination import paginate_query
from app.schemas.pagination import PaginatedResponse

router = APIRouter()

@router.get("/", response_model=PaginatedResponse[GenreRead])
def list_genres(
    db: Session = Depends(get_db),
    limit: int = 20,
    offset: int = 0,
    sort_by: str = "name",
    sort_order: str = "asc"
):
    query = db.query(Genre)
    total, items = paginate_query(query, Genre, limit, offset, sort_by, sort_order)
    return {"total": total, "items": items}

@router.post("/", response_model=GenreRead)
def create_genre(data: GenreCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    existing = db.query(Genre).filter_by(name=data.name).first()
    if existing:
        raise AlreadyExistsException("Genre already exists")
    genre = Genre(name=data.name)
    db.add(genre)
    db.commit()
    db.refresh(genre)
    return genre
