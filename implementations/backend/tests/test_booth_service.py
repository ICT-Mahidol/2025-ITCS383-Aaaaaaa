import pytest
from app.services.booth_service import create_booth, get_booths_by_event, get_booth_by_id, update_booth, delete_booth
from app.schemas.booth_schema import BoothCreate, BoothUpdate
from app.models.booth import BoothType, BoothClassification, DurationType, BoothStatus
from decimal import Decimal
from tests.factories import BoothFactory, EventFactory

def test_create_booth(db_session):
    event = EventFactory()
    db_session.add(event)
    db_session.commit()

    booth_data = BoothCreate(
        event_id=event.event_id,
        booth_number="A01",
        size="Medium",
        price=Decimal("100.00"),
        type=BoothType.INDOOR,
        classification=BoothClassification.TEMPORARY,
        duration_type=DurationType.SHORT_TERM
    )
    booth = create_booth(db_session, booth_data)

    assert booth.booth_number == "A01"
    assert booth.event_id == event.event_id
    assert booth.status == BoothStatus.AVAILABLE

def test_get_booths_by_event(db_session):
    event = EventFactory()
    db_session.add(event)

    booth1 = BoothFactory(event_id=event.event_id)
    booth2 = BoothFactory(event_id=event.event_id)
    db_session.add_all([booth1, booth2])
    db_session.commit()

    booths = get_booths_by_event(db_session, event.event_id)
    assert len(booths) == 2
    assert all(booth.event_id == event.event_id for booth in booths)

def test_get_booth_by_id(db_session):
    booth = BoothFactory()
    db_session.add(booth)
    db_session.commit()

    found_booth = get_booth_by_id(db_session, booth.booth_id)
    assert found_booth is not None
    assert found_booth.booth_id == booth.booth_id

def test_update_booth(db_session):
    booth = BoothFactory()
    db_session.add(booth)
    db_session.commit()

    update_data = BoothUpdate(status=BoothStatus.RESERVED)
    updated_booth = update_booth(db_session, booth.booth_id, update_data)

    assert updated_booth is not None
    assert updated_booth.status == BoothStatus.RESERVED

def test_delete_booth(db_session):
    booth = BoothFactory()
    db_session.add(booth)
    db_session.commit()

    deleted_booth = delete_booth(db_session, booth.booth_id)
    assert deleted_booth is not None

    found_booth = get_booth_by_id(db_session, booth.booth_id)
    assert found_booth is None