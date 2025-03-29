#routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserRead
from app.services import auth as auth_service
from app.dependencies.auth import get_current_user
from app.utils.security import create_access_token
from app.database import get_db

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(auth_service.User).filter_by(username=user_data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    return auth_service.register_user(
        db,
        username=user_data.username,
        password=user_data.password,
        role=user_data.role  # pass role along
    )

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserRead)
def get_me(user = Depends(get_current_user)):
    return user
