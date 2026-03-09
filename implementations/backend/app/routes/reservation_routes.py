from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db_connection import get_db
from app.services.reservation_service import create_reservation, get_reservations_by_merchant, get_reservation_by_id, update_reservation, cancel_reservation
from app.schemas.reservation_schema import ReservationCreate, ReservationUpdate, ReservationResponse

router = APIRouter()

@router.post("/", response_model=ReservationResponse)
def create_new_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    # TODO: Get current merchant from JWT token
    merchant_id = "dummy_merchant_id"  # Replace with actual merchant ID from token
    try:
        return create_reservation(db, reservation, merchant_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[ReservationResponse])
def read_user_reservations(db: Session = Depends(get_db)):
    # TODO: Get current merchant from JWT token
    merchant_id = "dummy_merchant_id"  # Replace with actual merchant ID from token
    reservations = get_reservations_by_merchant(db, merchant_id)
    return reservations

@router.get("/{reservation_id}", response_model=ReservationResponse)
def read_reservation(reservation_id: str, db: Session = Depends(get_db)):
    db_reservation = get_reservation_by_id(db, reservation_id)
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return db_reservation

@router.put("/{reservation_id}", response_model=ReservationResponse)
def update_existing_reservation(reservation_id: str, reservation: ReservationUpdate, db: Session = Depends(get_db)):
    db_reservation = update_reservation(db, reservation_id, reservation)
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return db_reservation

@router.delete("/{reservation_id}")
def cancel_existing_reservation(reservation_id: str, db: Session = Depends(get_db)):
    db_reservation = cancel_reservation(db, reservation_id)
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return {"message": "Reservation cancelled successfully"}