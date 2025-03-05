import pytest
from fastapi.testclient import TestClient
from main.main import app

client = TestClient(app)

def test_create_room():
    response = client.post("/rooms", json={
        "name": "Living Room",
        "floor": 1,
        "size": [20.5, 15.3],
        "house": "Beach House",
        "type": 2
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Room created"

def test_get_rooms():
    response = client.get("/rooms")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_room():
    response = client.put("/rooms/1", json={
        "id": 1,
        "name": "Updated Room",
        "floor": 2,
        "size": [25.0, 18.0],
        "house": "Beach House",
        "type": 3
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Room"

def test_delete_room():
    response = client.delete("/rooms/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Room deleted"
