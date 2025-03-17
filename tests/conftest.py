import pytest
from fastapi.testclient import TestClient
import sys
import os

# Ensure the main directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main.main import app  # Import the FastAPI app from main/main.py

@pytest.fixture(scope="function")
def client():
    return TestClient(app)
