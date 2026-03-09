from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from app.models.booth import BoothType, BoothClassification, DurationType, BoothStatus

class BoothBase(BaseModel):
    booth_number: str
    size: Optional[str] = None
    price: Decimal
    location: Optional[str] = None
    type: BoothType
    classification: BoothClassification
    duration_type: DurationType
    electricity: Optional[bool] = False
    water_supply: Optional[bool] = False
    outlets: Optional[int] = 0

class BoothCreate(BoothBase):
    event_id: str

class BoothUpdate(BoothBase):
    status: Optional[BoothStatus] = None

class BoothResponse(BoothBase):
    booth_id: str
    event_id: str
    status: BoothStatus

    class Config:
        from_attributes = True