from urllib.parse import quote

from src.app import activities


def test_unregister_removes_participant_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name)
    email = "michael@mergington.edu"
    endpoint = f"/activities/{encoded_activity_name}/signup"

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]


def test_unregister_returns_error_when_activity_not_found(client):
    # Arrange
    activity_name = "Unknown Club"
    encoded_activity_name = quote(activity_name)
    email = "student@mergington.edu"
    endpoint = f"/activities/{encoded_activity_name}/signup"

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_error_when_participant_not_enrolled(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name)
    email = "not-enrolled@mergington.edu"
    endpoint = f"/activities/{encoded_activity_name}/signup"

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == f"{email} is not signed up for {activity_name}"
