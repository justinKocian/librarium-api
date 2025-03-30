# models/user_books.py

from sqlalchemy import Column, Integer, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class ReadStatus(str, enum.Enum):
    unread = "unread"
    reading = "reading"
    read = "read"
    dnf = "dnf"

read_status_enum = SqlEnum(
    ReadStatus,
    name="readstatus",
    create_type=True,
    validate_strings=True,
    native_enum=True,
    metadata=Base.metadata,
    values_callable=lambda x: [e.value for e in x],
)

class UserBooks(Base):
    __tablename__ = "user_books"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"), primary_key=True)
    read_status = Column(read_status_enum, nullable=False)

    user = relationship("User", backref="user_books")
    book = relationship("Book", backref="user_books")
