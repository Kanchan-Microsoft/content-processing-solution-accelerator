import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from ContentProcessorAPI.app.main import app  # Import without `src.`

import datetime

from fastapi.testclient import TestClient

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "I'm alive!"}
    assert response.headers["Custom-Header"] == "liveness probe"

def test_startup_endpoint():
    response = client.get("/startup")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "Running for" in response.json()["message"]
