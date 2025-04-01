from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Union
from app.utils.security import create_access_token

from app.database import get_db
from app.schemas.user import UserRead, UserUpdate, UserWithTokenResponse
from app.models.user import User
from app.dependencies.auth import get_current_user, get_current_admin
from app.services import user as user_service
from app.core.exceptions import NotFoundException

router = APIRouter()

@router.get(
    "/",
    response_model=list[UserRead],
    summary="List all users",
    description="Retrieve a list of all users. Admin access is required."
)
def list_users(db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    return user_service.get_all_users(db)

@router.get(
    "/{id}",
    response_model=UserRead,
    summary="Get a user by ID",
    description="Retrieve details of a user by their ID. Admin access is required."
)
def get_user(id: int, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    user = user_service.get_user_by_id(db, id)
    if not user:
        raise NotFoundException("User not found")
    return user

@router.put(
    "/me",
    response_model=Union[UserRead, UserWithTokenResponse],
    summary="Update your own user account",
    description=(
        "Update your username or password. If the username changes, a new access token is generated. "
        "Only the authenticated user can update their own account."
    )
)
def update_self(
    update_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    original_username = current_user.username
    updated_user = user_service.update_user(
        db,
        current_user,
        username=update_data.username,
        password=update_data.password
    )

    if update_data.username and update_data.username != original_username:
        token = create_access_token(data={"sub": updated_user.username})
        return {
            "user": updated_user,
            "access_token": token,
            "token_type": "bearer"
        }

    return updated_user

@router.delete(
    "/me",
    summary="Delete your own account",
    description="Delete your own user account. This action is irreversible."
)
def delete_self(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_service.delete_user(db, current_user)
    return {"detail": "User account deleted"}

@router.delete(
    "/{id}",
    summary="Delete a user by ID",
    description="Delete a user by their ID. Admin access is required."
)
def delete_user(id: int, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    user = user_service.get_user_by_id(db, id)
    if not user:
        raise NotFoundException("User not found")
    user_service.delete_user(db, user)
    return {"detail": f"User {user.username} deleted"}
