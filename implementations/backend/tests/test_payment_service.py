import pytest
from app.services.payment_service import create_payment, get_payments_by_reservation, get_payment_by_id, update_payment
from app.schemas.payment_schema import PaymentCreate, PaymentUpdate
from app.models.payment import PaymentMethod, PaymentStatus
from app.models.reservation import ReservationStatus
from decimal import Decimal
from tests.factories import PaymentFactory, ReservationFactory

def test_create_payment(db_session):
    reservation = ReservationFactory()
    db_session.add(reservation)
    db_session.commit()

    payment_data = PaymentCreate(
        reservation_id=reservation.reservation_id,
        amount=Decimal("100.00"),
        method=PaymentMethod.CREDIT_CARD
    )
    payment = create_payment(db_session, payment_data)

    assert payment.reservation_id == reservation.reservation_id
    assert payment.amount == Decimal("100.00")
    assert payment.payment_status == PaymentStatus.PENDING

def test_get_payments_by_reservation(db_session):
    reservation = ReservationFactory()
    db_session.add(reservation)

    payment1 = PaymentFactory(reservation_id=reservation.reservation_id)
    payment2 = PaymentFactory(reservation_id=reservation.reservation_id)
    db_session.add_all([payment1, payment2])
    db_session.commit()

    payments = get_payments_by_reservation(db_session, reservation.reservation_id)
    assert len(payments) == 2

def test_update_payment_status(db_session):
    payment = PaymentFactory()
    reservation = ReservationFactory()
    db_session.add_all([payment, reservation])
    db_session.commit()

    # Link payment to reservation
    payment.reservation_id = reservation.reservation_id
    db_session.commit()

    update_data = PaymentUpdate(payment_status=PaymentStatus.APPROVED)
    updated_payment = update_payment(db_session, payment.payment_id, update_data)

    assert updated_payment is not None
    assert updated_payment.payment_status == PaymentStatus.APPROVED

    # Check reservation status updated
    db_session.refresh(reservation)
    assert reservation.status == ReservationStatus.CONFIRMED