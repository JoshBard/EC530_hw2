import pytest
from fastapi.testclient import TestClient
from main.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users", json={
        "name": "John Doe",
        "username": "johndoe",
        "phone": "123-456-7890",
        "email": "johndoe@example.com"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "User created"

def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_user():
    response = client.put("/users/1", json={
        "id": 1,
        "name": "Updated Name",
        "username": "updateduser",
        "phone": "987-654-3210",
        "email": "updated@example.com"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"

def test_delete_user():
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted"
