import pytest

def test_home_request(client):
    response = client.get("/api/home")
    assert b"Session User" in response.data

def test_api_login(client):
    response = client.post("api/login", json={
        "service": "postgres",
        "username": "babybear",
        "password": "password"
    })
    assert b'"code": 0' in response.data