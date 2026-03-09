import pytest
from app.services.reservation_service import create_reservation, get_reservations_by_merchant, get_reservation_by_id, update_reservation, cancel_reservation
from app.schemas.reservation_schema import ReservationCreate, ReservationUpdate
from app.models.reservation import ReservationType, ReservationStatus
from app.models.booth import BoothStatus
from tests.factories import ReservationFactory, BoothFactory, MerchantFactory

def test_create_reservation(db_session):
    booth = BoothFactory()
    merchant = MerchantFactory()
    db_session.add_all([booth, merchant])
    db_session.commit()

    reservation_data = ReservationCreate(
        booth_id=booth.booth_id,
        reservation_type=ReservationType.SHORT_TERM
    )
    reservation = create_reservation(db_session, reservation_data, merchant.merchant_id)

    assert reservation.booth_id == booth.booth_id
    assert reservation.merchant_id == merchant.merchant_id
    assert reservation.status == ReservationStatus.PENDING_PAYMENT

    # Check booth status updated
    db_session.refresh(booth)
    assert booth.status == BoothStatus.RESERVED

def test_create_reservation_unavailable_booth(db_session):
    booth = BoothFactory()
    booth.status = BoothStatus.RESERVED
    db_session.add(booth)
    db_session.commit()

    reservation_data = ReservationCreate(
        booth_id=booth.booth_id,
        reservation_type=ReservationType.SHORT_TERM
    )

    with pytest.raises(ValueError, match="Booth is not available"):
        create_reservation(db_session, reservation_data, "merchant123")

def test_get_reservations_by_merchant(db_session):
    merchant = MerchantFactory()
    db_session.add(merchant)

    reservation1 = ReservationFactory(merchant_id=merchant.merchant_id)
    reservation2 = ReservationFactory(merchant_id=merchant.merchant_id)
    db_session.add_all([reservation1, reservation2])
    db_session.commit()

    reservations = get_reservations_by_merchant(db_session, merchant.merchant_id)
    assert len(reservations) == 2

def test_cancel_reservation(db_session):
    booth = BoothFactory()
    reservation = ReservationFactory()
    db_session.add_all([booth, reservation])
    db_session.commit()

    cancelled = cancel_reservation(db_session, reservation.reservation_id)
    assert cancelled is not None
    assert cancelled.status == ReservationStatus.CANCELLED

    # Check booth status reverted
    db_session.refresh(booth)
    assert booth.status == BoothStatus.AVAILABLE