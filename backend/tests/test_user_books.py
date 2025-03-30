import pytest
from tests.test_factory import create_admin, create_book

@pytest.fixture(scope="module")
def book_and_user(client):
    headers = create_admin(client)
    book = create_book(client, headers)
    return {"headers": headers, "book_id": book["id"]}

def test_add_reading_status(client, book_and_user):
    res = client.post(
        "/user_books/",
        json={"book_id": book_and_user["book_id"], "read_status": "reading"},
        headers=book_and_user["headers"]
    )
    assert res.status_code == 200
    data = res.json()
    assert data["book_id"] == book_and_user["book_id"]
    assert data["read_status"] == "reading"

def test_get_reading_status(client, book_and_user):
    res = client.get(f"/user_books/{book_and_user['book_id']}", headers=book_and_user["headers"])
    assert res.status_code == 200
    assert res.json()["book_id"] == book_and_user["book_id"]

def test_update_reading_status(client, book_and_user):
    res = client.put(
        f"/user_books/{book_and_user['book_id']}",
        json={"read_status": "read"},
        headers=book_and_user["headers"]
    )
    assert res.status_code == 200
    assert res.json()["read_status"] == "read"

def test_list_reading_statuses(client, book_and_user):
    res = client.get("/user_books/", headers=book_and_user["headers"])
    assert res.status_code == 200
    statuses = res.json()
    assert any(s["book_id"] == book_and_user["book_id"] for s in statuses)

def test_delete_reading_status(client, book_and_user):
    res = client.delete(f"/user_books/{book_and_user['book_id']}", headers=book_and_user["headers"])
    assert res.status_code == 204

    # Confirm it's gone
    res = client.get(f"/user_books/{book_and_user['book_id']}", headers=book_and_user["headers"])
    assert res.status_code == 404
