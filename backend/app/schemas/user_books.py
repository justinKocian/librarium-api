# schemas/user_book.py

from pydantic import BaseModel
from enum import Enum

class ReadStatus(str, Enum):
    unread = "unread"
    reading = "reading"
    read = "read"
    dnf = "dnf"

class UserBookCreate(BaseModel):
    book_id: int
    read_status: ReadStatus

class UserBookUpdate(BaseModel):
    read_status: ReadStatus

class UserBookOut(BaseModel):
    user_id: int
    book_id: int
    read_status: ReadStatus

    model_config = {
        "from_attributes": True
    }