from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.models.payment import PaymentMethod, PaymentStatus

class PaymentBase(BaseModel):
    amount: Decimal
    method: PaymentMethod

class PaymentCreate(PaymentBase):
    reservation_id: str

class PaymentUpdate(BaseModel):
    payment_status: Optional[PaymentStatus] = None
    slip_url: Optional[str] = None

class PaymentResponse(PaymentBase):
    payment_id: str
    reservation_id: str
    payment_status: PaymentStatus
    slip_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True