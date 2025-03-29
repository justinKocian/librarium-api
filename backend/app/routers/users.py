from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserRead, UserUpdate
from app.models.user import User
from app.dependencies.auth import get_current_user, get_current_admin
from app.services import user as user_service

router = APIRouter()

@router.get("/", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    return user_service.get_all_users(db)

@router.get("/{id}", response_model=UserRead)
def get_user(id: int, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    user = user_service.get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/me", response_model=UserRead)
def update_self(update_data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return user_service.update_user(db, current_user, update_data.username, update_data.password)

@router.delete("/me")
def delete_self(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_service.delete_user(db, current_user)
    return {"detail": "User account deleted"}

@router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    user = user_service.get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_service.delete_user(db, user)
    return {"detail": f"User {user.username} deleted"}
