#services/auth.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.auth import TokenData
from app.utils.security import get_password_hash, verify_password, create_access_token
from app.schemas.user import UserOut
from app.models.user import UserRole


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_token(user: User):
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


def get_user_by_token(db: Session, token_data: TokenData) -> User:
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def register_user(db: Session, username: str, password: str, role: UserRole = UserRole.regular) -> UserOut:
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_pw = get_password_hash(password)
    new_user = User(username=username, hashed_password=hashed_pw, role=role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
