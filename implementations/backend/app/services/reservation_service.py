from sqlalchemy.orm import Session
import uuid
from app.models.reservation import Reservation, ReservationStatus
from app.models.booth import Booth, BoothStatus
from app.schemas.reservation_schema import ReservationCreate, ReservationUpdate

def create_reservation(db: Session, reservation: ReservationCreate, merchant_id: str):
    # Check if booth is available
    booth = db.query(Booth).filter(Booth.booth_id == reservation.booth_id).first()
    if not booth or booth.status != BoothStatus.AVAILABLE:
        raise ValueError("Booth is not available")

    db_reservation = Reservation(
        reservation_id=str(uuid.uuid4()),
        booth_id=reservation.booth_id,
        merchant_id=merchant_id,
        reservation_type=reservation.reservation_type
    )
    db.add(db_reservation)

    # Update booth status
    booth.status = BoothStatus.RESERVED
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def get_reservations_by_merchant(db: Session, merchant_id: str):
    return db.query(Reservation).filter(Reservation.merchant_id == merchant_id).all()

def get_reservation_by_id(db: Session, reservation_id: str):
    return db.query(Reservation).filter(Reservation.reservation_id == reservation_id).first()

def update_reservation(db: Session, reservation_id: str, reservation: ReservationUpdate):
    db_reservation = db.query(Reservation).filter(Reservation.reservation_id == reservation_id).first()
    if db_reservation:
        for key, value in reservation.dict(exclude_unset=True).items():
            setattr(db_reservation, key, value)
        db.commit()
        db.refresh(db_reservation)
    return db_reservation

def cancel_reservation(db: Session, reservation_id: str):
    db_reservation = db.query(Reservation).filter(Reservation.reservation_id == reservation_id).first()
    if db_reservation:
        db_reservation.status = ReservationStatus.CANCELLED
        # Make booth available again
        booth = db_reservation.booth
        booth.status = BoothStatus.AVAILABLE
        db.commit()
    return db_reservation