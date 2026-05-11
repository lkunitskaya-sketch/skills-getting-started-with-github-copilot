from urllib.parse import quote

from src.app import activities


def test_signup_adds_participant_to_activity(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name)
    email = "newstudent@mergington.edu"
    endpoint = f"/activities/{encoded_activity_name}/signup"

    # Act
    response = client.post(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]


def test_signup_returns_error_when_activity_not_found(client):
    # Arrange
    activity_name = "Unknown Club"
    encoded_activity_name = quote(activity_name)
    email = "student@mergington.edu"
    endpoint = f"/activities/{encoded_activity_name}/signup"

    # Act
    response = client.post(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_error_for_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name)
    email = "michael@mergington.edu"
    endpoint = f"/activities/{encoded_activity_name}/signup"

    # Act
    response = client.post(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == f"{email} is already signed up for {activity_name}"
