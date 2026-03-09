from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.reservation import ReservationType, ReservationStatus

class ReservationBase(BaseModel):
    booth_id: str
    reservation_type: ReservationType

class ReservationCreate(ReservationBase):
    pass

class ReservationUpdate(BaseModel):
    status: Optional[ReservationStatus] = None

class ReservationResponse(ReservationBase):
    reservation_id: str
    merchant_id: str
    status: ReservationStatus
    created_at: datetime

    class Config:
        from_attributes = True