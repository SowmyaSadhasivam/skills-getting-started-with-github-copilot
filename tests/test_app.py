import pytest
from fastapi.testclient import TestClient

import copy
from src.app import app, activities as app_activities

client = TestClient(app)

# Original activities data for test resets
ORIGINAL_ACTIVITIES = {
    "Tennis Club": {
        "description": "Tennis lessons and competitive matches",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["alex@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Basketball practice and inter-school competitions",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["james@mergington.edu", "marcus@mergington.edu"]
    },
    "Art Studio": {
        "description": "Painting, drawing, and visual arts creation",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["isabella@mergington.edu"]
    },
    "Music Band": {
        "description": "Learn instruments and perform in concerts",
        "schedule": "Mondays and Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["lucas@mergington.edu", "amelia@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop argumentation and public speaking skills",
        "schedule": "Tuesdays, 3:30 PM - 4:45 PM",
        "max_participants": 14,
        "participants": ["noah@mergington.edu"]
    },
    "Science Club": {
        "description": "Explore STEM topics through experiments and projects",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["chloe@mergington.edu", "ethan@mergington.edu"]
    },
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}

@pytest.fixture(autouse=True)
def reset_activities():
    app_activities.clear()
    app_activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Tennis Club" in data

def test_signup_and_unregister():
    activity = "Tennis Club"
    email = "testuser@mergington.edu"
    # Ensure not already signed up
    client.post(f"/activities/{activity}/unregister", params={"email": email})
    # Sign up
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Duplicate signup should fail
    response2 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response2.status_code == 400
    # Unregister
    response3 = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response3.status_code == 200
    assert f"Unregistered {email}" in response3.json()["message"]
    # Unregister again should fail
    response4 = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response4.status_code == 404

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup", params={"email": "foo@bar.com"})
    assert response.status_code == 404

def test_unregister_activity_not_found():
    response = client.post("/activities/Nonexistent/unregister", params={"email": "foo@bar.com"})
    assert response.status_code == 404
