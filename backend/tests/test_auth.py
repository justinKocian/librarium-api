from tests.test_factory import register_user, login_user

def test_user_can_register(client):
    res = client.post("/auth/register", json={
        "username": "newuser",
        "password": "securepass",
        "role": "regular"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["username"] == "newuser"
    assert "id" in data

def test_duplicate_username_fails(client):
    # "newuser" was registered in the previous test
    res = client.post("/auth/register", json={
        "username": "newuser",
        "password": "anotherpass",
        "role": "regular"
    })
    assert res.status_code == 400
    assert res.json()["detail"] == "Username already exists"

def test_user_can_login(client):
    res = client.post("/auth/login", data={
        "username": "newuser",
        "password": "securepass"
    })
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data

def test_me_returns_current_user(client):
    headers = login_user(client, username="newuser", password="securepass")
    res = client.get("/auth/me", headers=headers)
    assert res.status_code == 200
    assert res.json()["username"] == "newuser"

def test_user_can_update_their_own_account(client):
    headers = login_user(client, "newuser", "securepass")
    res = client.put("/users/me", json={"username": "updateduser"}, headers=headers)
    assert res.status_code == 200

    data = res.json()
    if "user" in data:
        assert data["user"]["username"] == "updateduser"
    else:
        assert data["username"] == "updateduser"


def test_updated_user_can_still_authenticate(client):
    # Login with updated username
    register_user(client, "tempuser", "temppass")
    res = client.post("/auth/login", data={
        "username": "updateduser",
        "password": "securepass"
    })
    assert res.status_code == 200
    assert "access_token" in res.json()
