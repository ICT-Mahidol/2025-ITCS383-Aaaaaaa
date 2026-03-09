from sqlalchemy.orm import Session
import uuid
from app.models.payment import Payment, PaymentStatus
from app.models.reservation import Reservation, ReservationStatus
from app.schemas.payment_schema import PaymentCreate, PaymentUpdate

def create_payment(db: Session, payment: PaymentCreate):
    db_payment = Payment(
        payment_id=str(uuid.uuid4()),
        reservation_id=payment.reservation_id,
        amount=payment.amount,
        method=payment.method
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_payments_by_reservation(db: Session, reservation_id: str):
    return db.query(Payment).filter(Payment.reservation_id == reservation_id).all()

def get_payment_by_id(db: Session, payment_id: str):
    return db.query(Payment).filter(Payment.payment_id == payment_id).first()

def update_payment(db: Session, payment_id: str, payment: PaymentUpdate):
    db_payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    if db_payment:
        for key, value in payment.dict(exclude_unset=True).items():
            setattr(db_payment, key, value)
            # If payment is approved, update reservation status
            if key == 'payment_status' and value == PaymentStatus.APPROVED:
                reservation = db_payment.reservation
                reservation.status = ReservationStatus.CONFIRMED
        db.commit()
        db.refresh(db_payment)
    return db_payment