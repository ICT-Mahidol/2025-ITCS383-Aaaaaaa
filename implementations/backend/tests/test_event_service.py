import pytest
from app.services.event_service import create_event, get_events, get_event_by_id, update_event, delete_event
from app.schemas.event_schema import EventCreate, EventUpdate
from datetime import date
from tests.factories import EventFactory

def test_create_event(db_session):
    event_data = EventCreate(
        name="Test Event",
        description="A test event",
        location="Test Location",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 1, 2)
    )
    event = create_event(db_session, event_data, "user123")

    assert event.name == "Test Event"
    assert event.created_by == "user123"
    assert event.event_id is not None

def test_get_events(db_session):
    # Create multiple events
    event1 = EventFactory()
    event2 = EventFactory()
    db_session.add_all([event1, event2])
    db_session.commit()

    events = get_events(db_session)
    assert len(events) >= 2

def test_get_event_by_id(db_session):
    event = EventFactory()
    db_session.add(event)
    db_session.commit()

    found_event = get_event_by_id(db_session, event.event_id)
    assert found_event is not None
    assert found_event.event_id == event.event_id

    not_found = get_event_by_id(db_session, "nonexistent")
    assert not_found is None

def test_update_event(db_session):
    event = EventFactory()
    db_session.add(event)
    db_session.commit()

    update_data = EventUpdate(name="Updated Event")
    updated_event = update_event(db_session, event.event_id, update_data)

    assert updated_event is not None
    assert updated_event.name == "Updated Event"

def test_delete_event(db_session):
    event = EventFactory()
    db_session.add(event)
    db_session.commit()

    deleted_event = delete_event(db_session, event.event_id)
    assert deleted_event is not None

    # Check it's deleted
    found_event = get_event_by_id(db_session, event.event_id)
    assert found_event is None