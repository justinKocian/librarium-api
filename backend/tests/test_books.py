import pytest

BOOK_DATA = {
    "title": "The Beacon of The Hollow",
    "author": "J. David Kocian",
    "isbn": "9780441013593",
    "genre_id": 1,
    "series_id": 1,
    "volume": 1,
    "tag_ids": [1, 2],
    "cover_path": "uploads/0d120ab8cf9a40e68fbaf59be0633e25.jpg"
}


@pytest.fixture(scope="module")
def auth_headers(client):
    # Register user with admin role
    register = client.post("/auth/register", json={
        "username": "adminguy",
        "password": "secret123",
        "role": "admin"
    })
    assert register.status_code == 200

    # Login and get token
    login = client.post("/auth/login", data={
        "username": "adminguy",
        "password": "secret123"
    })
    assert login.status_code == 200

    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="module")
def create_book(client, auth_headers):
    # Set up required metadata
    client.post("/genres/", json={"name": "Horror"}, headers=auth_headers)
    client.post("/tags/", json={"name": "Family"}, headers=auth_headers)
    client.post("/tags/", json={"name": "Supernatural"}, headers=auth_headers)
    client.post("/tags/", json={"name": "Fantasy"}, headers=auth_headers)
    client.post("/tags/", json={"name": "Comedy"}, headers=auth_headers)
    client.post("/series/", json={"name": "The Hollow"}, headers=auth_headers)

    # Add the book
    response = client.post("/books/", json=BOOK_DATA, headers=auth_headers)
    assert response.status_code == 200
    return response.json()


def test_search_by_title(client, create_book, auth_headers):
    response = client.get("/books/search?q=beacon", headers=auth_headers)
    assert response.status_code == 200
    books = response.json()
    assert any("Beacon" in b["title"] for b in books)


def test_search_by_genre(client, create_book, auth_headers):
    response = client.get("/books/search?genre_id=1", headers=auth_headers)
    assert response.status_code == 200
    books = response.json()
    assert any(b["genre"]["name"] == "Horror" for b in books)


def test_search_by_tag(client, create_book, auth_headers):
    response = client.get("/books/search?tag_ids=1&tag_ids=2", headers=auth_headers)
    assert response.status_code == 200
    books = response.json()
    assert any(
        any(t["name"] in ["Family", "Supernatural"] for t in b["tags"])
        for b in books
    )


def test_search_by_series(client, create_book, auth_headers):
    response = client.get("/books/search?series_id=1", headers=auth_headers)
    assert response.status_code == 200
    books = response.json()
    assert any(b["series"]["name"] == "The Hollow" for b in books)


def test_search_by_volume(client, create_book, auth_headers):
    response = client.get("/books/search?volume=1", headers=auth_headers)
    assert response.status_code == 200
    books = response.json()
    assert any(b["volume"] == 1 for b in books)
