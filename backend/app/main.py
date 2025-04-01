from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from dotenv import load_dotenv

from app.core.logging_config import setup_logging
from app.middleware.logging_middleware import LoggingMiddleware
from app.core import error_handlers
from app.database import Base, engine
from app.routers import auth, users, books, genres, tags, series, upload, user_books

from fastapi import Request
from fastapi.responses import JSONResponse  # For rate-limit exceeded response handling

# Load environment variables
load_dotenv()

# Set up logging first
setup_logging()
logger = logging.getLogger(__name__)

# Define metadata for OpenAPI tags
tags_metadata = [
    {"name": "Authentication", "description": "Endpoints for user registration, login, and identity lookup."},
    {"name": "Users", "description": "Admin-only user management and account operations."},
    {"name": "Books", "description": "Create, retrieve, update, delete, and search books."},
    {"name": "Genres", "description": "Manage genre metadata (admin only)."},
    {"name": "Tags", "description": "Manage tag metadata and assign tags to books (admin only)."},
    {"name": "Series", "description": "Manage book series metadata (admin only)."},
    {"name": "Cover Uploads", "description": "Upload and delete book cover images."},
    {"name": "Reading Status", "description": "Track reading progress per user per book."}
]

# Create DB tables
Base.metadata.create_all(bind=engine)

# Define lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup complete.")
    error_handlers.register(app)  # Register custom error handlers
    yield
    logger.info("Application shutdown complete.")

# Initialize the app with lifespan handler
app = FastAPI(lifespan=lifespan)

# Logging Middleware
app.add_middleware(LoggingMiddleware)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend's URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(genres.router, prefix="/genres", tags=["Genres"])
app.include_router(tags.router, prefix="/tags", tags=["Tags"])
app.include_router(series.router, prefix="/series", tags=["Series"])
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(user_books.router, prefix="/user_books", tags=["UserBooks"])

# Health check route
@app.get("/")
def health():
    return {"status": "ok"}
