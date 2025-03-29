#models/book.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=True)
    genre_id = Column(Integer, ForeignKey("genres.id"))
    series_id = Column(Integer, ForeignKey("series.id"), nullable=True)
    volume = Column(Integer, nullable=True)
    cover_path = Column(String, nullable=True)
    read_status = Column(String, nullable=True) 

    genre = relationship("Genre", back_populates="books")
    series = relationship("Series", back_populates="books")
    tags = relationship("Tag", secondary="book_tags", back_populates="books")
