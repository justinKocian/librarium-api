from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.security import get_password_hash

def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db: Session):
    return db.query(User).all()

def update_user(db: Session, user: User, username: str = None, password: str = None):
    if username:
        user.username = username
    if password:
        user.hashed_password = get_password_hash(password)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()
