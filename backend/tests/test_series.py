from tests.test_factory import create_admin

def test_admin_can_create_series(client):
    headers = create_admin(client)
    res = client.post("/series/", json={"name": "Galactic Tales"}, headers=headers)
    assert res.status_code == 200
    assert res.json()["name"] == "Galactic Tales"

def test_admin_can_list_series(client):
    headers = create_admin(client)
    res = client.get("/series/", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "total" in data
    assert isinstance(data["items"], list)
