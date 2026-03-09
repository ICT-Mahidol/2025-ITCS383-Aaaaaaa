import pytest
from app.models.user import User, UserRole
from app.models.event import Event
from app.models.booth import Booth, BoothType, BoothClassification, DurationType, BoothStatus
from tests.factories import UserFactory, EventFactory, BoothFactory

def test_user_creation(db_session):
    user = UserFactory()
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.id is not None
    assert user.username is not None
    assert user.role == UserRole.GENERAL_USER

def test_event_creation(db_session):
    event = EventFactory()
    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)

    assert event.event_id is not None
    assert event.name is not None
    assert event.start_date <= event.end_date

def test_booth_creation(db_session):
    booth = BoothFactory()
    db_session.add(booth)
    db_session.commit()
    db_session.refresh(booth)

    assert booth.booth_id is not None
    assert booth.status == BoothStatus.AVAILABLE
    assert booth.price > 0