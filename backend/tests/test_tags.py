from tests.test_factory import create_admin


def test_admin_can_create_tag(client):
    headers = create_admin(client)
    res = client.post("/tags/", json={"name": "Space"}, headers=headers)
    assert res.status_code == 200
    assert res.json()["name"] == "Space"


def test_admin_can_list_tags(client):
    headers = create_admin(client)
    res = client.get("/tags/", headers=headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)
