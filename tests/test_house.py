import pytest
from fastapi.testclient import TestClient
from main.main import app

client = TestClient(app)

def test_create_house():
    response = client.post("/houses", json={
        "name": "Beach House",
        "address": "123 Ocean Ave",
        "location": [34.0522, -118.2437],
        "owner": "John Doe",
        "occupants": ["Alice", "Bob"]
    })
    assert response.status_code == 200
    assert response.json()["message"] == "House created"

def test_get_houses():
    response = client.get("/houses")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_house():
    response = client.put("/houses/1", json={
        "id": 1,
        "name": "Updated House",
        "address": "456 New St",
        "location": [38.0, -123.0],
        "owner": "Jane Doe",
        "occupants": ["Charlie", "Dave"]
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Updated House"

def test_delete_house():
    response = client.delete("/houses/1")
    assert response.status_code == 200
    assert response.json()["message"] == "House deleted"
