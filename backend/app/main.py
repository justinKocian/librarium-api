from fastapi import FastAPI
from app.routers import auth, users, books, genres, tags, series, upload
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(genres.router, prefix="/genres", tags=["Genres"])
app.include_router(tags.router, prefix="/tags", tags=["Tags"])
app.include_router(series.router, prefix="/series", tags=["Series"])
app.include_router(upload.router, prefix="/upload", tags=["Upload"])

@app.get("/")
def ping():
    return {"status": "ok"}
