from unittest.mock import patch

# Patch BEFORE any other imports that might load Azure SDK
patch_target = "ContentProcessorAPI.app.libs.app_configuration.helper.AppConfigurationHelper.read_and_set_environmental_variables"
with patch(patch_target):
    import sys
    import os
    import datetime

    # Add project root to path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

    from ContentProcessorAPI.app.main import app  # Import AFTER mocking

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
