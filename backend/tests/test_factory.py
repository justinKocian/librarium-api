# backend/tests/test_factory.py

import uuid
from fastapi.testclient import TestClient
from app.schemas.user import UserRole
from app.models.user import User
from app.database import SessionLocal
from app.utils.security import get_password_hash


def register_user(client: TestClient, username="testuser", password="testpass"):
    res = client.post("/auth/register", json={
        "username": username,
        "password": password
    })
    assert res.status_code == 200
    return res.json()


def login_user(client: TestClient, username="testuser", password="testpass"):
    res = client.post("/auth/login", data={
        "username": username,
        "password": password
    })
    assert res.status_code == 200
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_admin(client: TestClient, username="admin", password="adminpass"):
    db = SessionLocal()
    existing = db.query(User).filter_by(username=username).first()
    if not existing:
        admin = User(
            username=username,
            hashed_password=get_password_hash(password),
            role=UserRole.admin.value
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
    db.close()
    return login_user(client, username, password)


def setup_metadata(client: TestClient, headers):
    client.post("/genres/", json={"name": "Horror"}, headers=headers)
    client.post("/tags/", json={"name": "Supernatural"}, headers=headers)
    client.post("/series/", json={"name": "The Hollow"}, headers=headers)


def create_book(client: TestClient, headers):
    setup_metadata(client, headers)

    unique_isbn = f"978-{uuid.uuid4().int % 10000000000:010d}"  # Ensures a unique 13-digit ISBN

    book_data = {
        "title": "The Beacon of The Hollow",
        "author": "J. David Kocian",
        "isbn": unique_isbn,
        "genre_id": 1,
        "series_id": 1,
        "volume": 1,
        "tag_ids": [1],
        "cover_path": "app/tests/test_cover.jpg"
    }

    res = client.post("/books/", json=book_data, headers=headers)
    assert res.status_code == 200
    return res.json()
