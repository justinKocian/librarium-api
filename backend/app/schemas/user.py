from pydantic import BaseModel
from enum import Enum
from typing import Optional


class UserRole(str, Enum):
    admin = "admin"
    regular = "regular"


class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole = UserRole.regular


class UserOut(BaseModel):
    id: int
    username: str
    role: UserRole

    class Config:
        from_attributes = True  # replaces orm_mode in Pydantic v2


class UserRead(UserOut):
    pass


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
