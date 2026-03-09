from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
import shutil
import os
from app.database.db_connection import get_db
from app.services.payment_service import create_payment, get_payments_by_reservation, get_payment_by_id, update_payment
from app.schemas.payment_schema import PaymentCreate, PaymentUpdate, PaymentResponse

router = APIRouter()

@router.post("/", response_model=PaymentResponse)
def create_new_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    return create_payment(db, payment)

@router.get("/reservation/{reservation_id}", response_model=list[PaymentResponse])
def read_payments_by_reservation(reservation_id: str, db: Session = Depends(get_db)):
    payments = get_payments_by_reservation(db, reservation_id)
    return payments

@router.get("/{payment_id}", response_model=PaymentResponse)
def read_payment(payment_id: str, db: Session = Depends(get_db)):
    db_payment = get_payment_by_id(db, payment_id)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment

@router.put("/{payment_id}", response_model=PaymentResponse)
def update_existing_payment(payment_id: str, payment: PaymentUpdate, db: Session = Depends(get_db)):
    db_payment = update_payment(db, payment_id, payment)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment

@router.post("/upload-slip")
def upload_payment_slip(file: UploadFile = File(...)):
    # Save the uploaded file
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"slip_url": file_path}