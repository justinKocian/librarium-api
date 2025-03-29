from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagRead
from app.dependencies.auth import get_current_admin
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=list[TagRead])
def list_tags(db: Session = Depends(get_db)):
    return db.query(Tag).all()

@router.post("/", response_model=TagRead)
def create_tag(data: TagCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    existing = db.query(Tag).filter_by(name=data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tag already exists")
    tag = Tag(name=data.name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag
