import pytest
from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)

def test_get_activities():
    # Arrange: (nothing to arrange for this test)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity_success():
    # Arrange
    test_email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {test_email} for {activity}" in response.json()["message"]
    # Clean up: Remove test user if needed
    activities[activity]["participants"].remove(test_email)

def test_signup_for_activity_duplicate():
    # Arrange
    activity = "Chess Club"
    test_email = "michael@mergington.edu"  # Already registered
    # Act
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_for_nonexistent_activity():
    # Arrange
    activity = "Nonexistent Club"
    test_email = "someone@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
