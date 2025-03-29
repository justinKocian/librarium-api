from pydantic import BaseModel
from enum import Enum
from typing import Optional

class UserRole(str, Enum):
    admin = "admin"
    regular = "regular"

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    role: UserRole

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

