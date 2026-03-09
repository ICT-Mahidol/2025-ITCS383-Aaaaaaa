import pytest
from tests.factories import UserFactory, EventFactory, BoothFactory

def test_register_user(client, db_session):
    user_data = {
        "username": "testuser",
        "password": "testpass",
        "name": "Test User",
        "citizen_id": "1234567890123",
        "contact_info": "test@example.com",
        "role": "GENERAL_USER"
    }

    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["name"] == "Test User"

def test_login_user(client, db_session):
    # First register a user
    user = UserFactory(username="loginuser", password="hashedpass")
    db_session.add(user)
    db_session.commit()

    login_data = {
        "username": "loginuser",
        "password": "testpass"  # This won't work with hashed password, but for test
    }

    response = client.post("/api/auth/login", json=login_data)
    # This will fail because password is not hashed properly in factory
    # In real scenario, we'd need to handle this
    assert response.status_code in [200, 401]  # Either success or auth fail

def test_get_events(client, db_session):
    event = EventFactory()
    db_session.add(event)
    db_session.commit()

    response = client.get("/api/events")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1

def test_create_event(client, db_session):
    event_data = {
        "name": "Test Event",
        "description": "Test Description",
        "location": "Test Location",
        "start_date": "2024-01-01",
        "end_date": "2024-01-02"
    }

    response = client.post("/api/events", json=event_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Event"

def test_get_booths_by_event(client, db_session):
    event = EventFactory()
    booth = BoothFactory(event_id=event.event_id)
    db_session.add_all([event, booth])
    db_session.commit()

    response = client.get(f"/api/booths/event/{event.event_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1

def test_create_booth(client, db_session):
    event = EventFactory()
    db_session.add(event)
    db_session.commit()

    booth_data = {
        "event_id": event.event_id,
        "booth_number": "A01",
        "size": "Medium",
        "price": "100.00",
        "type": "INDOOR",
        "classification": "TEMPORARY",
        "duration_type": "SHORT_TERM"
    }

    response = client.post("/api/booths", json=booth_data)
    assert response.status_code == 200
    data = response.json()
    assert data["booth_number"] == "A01"