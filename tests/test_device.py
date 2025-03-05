import pytest
from fastapi.testclient import TestClient
from main.main import app

client = TestClient(app)

def test_create_device():
    response = client.post("/devices", json={
        "name": "Smart Light",
        "room": "Living Room",
        "type": 1,
        "setting": "On",
        "data": [100, 200, 300],
        "status": "Active"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Device created"
    assert response.json()["device"]["name"] == "Smart Light"

def test_get_devices():
    response = client.get("/devices")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0  # Ensure at least one device exists

def test_update_device():
    response = client.put("/devices/1", json={
        "id": 1,
        "name": "Updated Light",
        "room": "Living Room",
        "type": 2,
        "setting": "Dimmed",
        "data": [150, 250, 350],
        "status": "Inactive"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Light"

def test_delete_device():
    response = client.delete("/devices/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Device deleted"
