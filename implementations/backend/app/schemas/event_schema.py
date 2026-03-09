from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class EventBase(BaseModel):
    name: str
    description: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    pass

class EventResponse(EventBase):
    event_id: str
    created_by: str
    created_at: datetime

    class Config:
        from_attributes = True