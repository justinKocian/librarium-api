from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.series import Series
from app.schemas.series import SeriesCreate, SeriesRead
from app.dependencies.auth import get_current_admin
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=list[SeriesRead])
def list_series(db: Session = Depends(get_db)):
    return db.query(Series).all()

@router.post("/", response_model=SeriesRead)
def create_series(data: SeriesCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    existing = db.query(Series).filter_by(name=data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Series already exists")
    series = Series(name=data.name)
    db.add(series)
    db.commit()
    db.refresh(series)
    return series
