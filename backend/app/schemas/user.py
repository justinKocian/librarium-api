from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)


class UserRead(UserOut):
    pass


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None


class UserWithTokenResponse(BaseModel):
    user: UserRead
    access_token: str
    token_type: str = "bearer"
