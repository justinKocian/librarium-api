def test_register_user(client):
    response = client.post("/auth/register", json={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data
    assert data["role"] == "regular"
