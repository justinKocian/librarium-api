def test_ping(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}
