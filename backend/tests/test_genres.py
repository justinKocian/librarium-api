from tests.test_factory import create_admin


def test_admin_can_create_genre(client):
    headers = create_admin(client)
    res = client.post("/genres/", json={"name": "Sci-Fi"}, headers=headers)
    assert res.status_code == 200
    assert res.json()["name"] == "Sci-Fi"


def test_admin_can_list_genres(client):
    headers = create_admin(client)
    res = client.get("/genres/", headers=headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)
