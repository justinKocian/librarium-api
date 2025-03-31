from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.series import Series
from app.schemas.series import SeriesCreate, SeriesRead
from app.dependencies.auth import get_current_admin
from app.database import get_db
from app.core.exceptions import AlreadyExistsException
from app.utils.pagination import paginate_query
from app.schemas.pagination import PaginatedResponse

router = APIRouter()

@router.get("/", response_model=PaginatedResponse[SeriesRead])
def list_series(
    db: Session = Depends(get_db),
    limit: int = 20,
    offset: int = 0,
    sort_by: str = "name",
    sort_order: str = "asc"
):
    query = db.query(Series)
    total, items = paginate_query(query, Series, limit, offset, sort_by, sort_order)
    return {"total": total, "items": items}


@router.post("/", response_model=SeriesRead)
def create_series(data: SeriesCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    existing = db.query(Series).filter_by(name=data.name).first()
    if existing:
        raise AlreadyExistsException("Series already exists")
    series = Series(name=data.name)
    db.add(series)
    db.commit()
    db.refresh(series)
    return series
