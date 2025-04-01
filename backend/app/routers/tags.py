from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagRead
from app.dependencies.auth import get_current_admin
from app.database import get_db
from app.core.exceptions import AlreadyExistsException
from app.utils.pagination import paginate_query
from app.schemas.pagination import PaginatedResponse

router = APIRouter()

@router.get(
    "/",
    response_model=PaginatedResponse[TagRead],
    summary="List all tags",
    description=(
        "Retrieve a paginated list of all available tags. "
        "Supports sorting by any field such as 'name'."
    )
)
def list_tags(
    db: Session = Depends(get_db),
    limit: int = 20,
    offset: int = 0,
    sort_by: str = "name",
    sort_order: str = "asc"
):
    query = db.query(Tag)
    total, items = paginate_query(query, Tag, limit, offset, sort_by, sort_order)
    return PaginatedResponse(total=total, items=items)  # Return PaginatedResponse instead of a dict

@router.post(
    "/",
    response_model=TagRead,
    summary="Create a new tag",
    description="Create a new tag in the catalog. Admin only. Checks if the tag already exists before creating."
)
def create_tag(data: TagCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    existing = db.query(Tag).filter_by(name=data.name).first()
    if existing:
        raise AlreadyExistsException("Tag already exists")
    tag = Tag(name=data.name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag
