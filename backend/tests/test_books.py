import pytest
import uuid
from tests.test_factory import create_admin, create_book

unique_isbn = f"978-{uuid.uuid4().int % 10000000000:010d}"  # Ensures a unique 13-digit ISBN

BOOK_PAYLOAD = {
        "title": "The Beacon of The Hollow",
        "author": "J. David Kocian",
        "isbn": unique_isbn,
        "genre_id": 1,
        "series_id": 1,
        "volume": 1,
        "tag_ids": [1],
        "cover_path": "app/tests/test_cover.jpg"
    }


def test_create_and_get_book(client):
    headers = create_admin(client)
    book = create_book(client, headers)

    res = client.get(f"/books/{book['id']}", headers=headers)
    assert res.status_code == 200
    assert res.json()["title"] == book["title"]


def test_list_books(client):
    headers = create_admin(client)
    res = client.get("/books/", headers=headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert any("Hollow" in b["title"] for b in res.json())


def test_update_book(client):
    headers = create_admin(client)
    book = create_book(client, headers)

    update = {"title": "The Beacon of The Hollow – Revised"}
    res = client.put(f"/books/{book['id']}", json=update, headers=headers)
    assert res.status_code == 200
    assert res.json()["title"] == update["title"]


def test_delete_book(client):
    headers = create_admin(client)
    book = create_book(client, headers)

    res = client.delete(f"/books/{book['id']}", headers=headers)
    assert res.status_code == 200
    assert "deleted" in res.json()["detail"]

    # Confirm it's gone
    res = client.get(f"/books/{book['id']}", headers=headers)
    assert res.status_code == 404
