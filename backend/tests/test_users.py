from tests.test_factory import create_admin, register_user


def test_admin_can_get_user_by_id(client):
    admin_headers = create_admin(client)
    user = register_user(client, "lookup_user", "pass123")

    res = client.get(f"/users/{user['id']}", headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["username"] == "lookup_user"


def test_admin_gets_404_for_invalid_user(client):
    admin_headers = create_admin(client)
    res = client.get("/users/9999", headers=admin_headers)
    assert res.status_code == 404


def test_admin_can_delete_user(client):
    admin_headers = create_admin(client)
    user = register_user(client, "tobedeleted", "pass123")

    res = client.delete(f"/users/{user['id']}", headers=admin_headers)
    assert res.status_code == 200
    assert "deleted" in res.json()["detail"]

    # Confirm deletion
    res = client.get(f"/users/{user['id']}", headers=admin_headers)
    assert res.status_code == 404
