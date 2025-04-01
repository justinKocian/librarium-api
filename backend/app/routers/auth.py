from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
import os

from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserRead, UserRole
from app.services import auth as auth_service
from app.dependencies.auth import get_current_user
from app.utils.security import create_access_token
from app.database import get_db
from app.core.exceptions import AlreadyExistsException, UnauthorizedException

router = APIRouter()

# REGISTER
@router.post(
    "/register",
    response_model=UserRead,
    summary="Register a new user",
    description="Creates a new user account. The role will default to 'regular' unless admin registration is explicitly allowed via environment variable."
)
async def register(request: Request, user_data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(auth_service.User).filter_by(username=user_data.username).first()
    if existing:
        raise AlreadyExistsException("Username already exists")
    allow_admin = os.getenv("ALLOW_ADMIN_REGISTRATION", "false").lower() == "true"
    role = user_data.role if user_data.role == UserRole.admin and allow_admin else UserRole.regular

    return auth_service.register_user(
        db,
        username=user_data.username,
        password=user_data.password,
        role=role
    )


# Apply rate limiting to the POST login route with the "request" argument
@router.post(
    "/login",
    response_model=Token,
    summary="Log in to get a token",
    description="Authenticates the user and returns a JWT access token. Used for all authorized endpoints."
)
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise UnauthorizedException("Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


# Apply rate limiting to the GET /me route with the "request" argument
@router.get(
    "/me",
    response_model=UserRead,
    summary="Get current user",
    description="Returns the currently authenticated user's information. Requires a valid token."
)
async def get_me(request: Request, user = Depends(get_current_user)):
    return user
