from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db_connection import get_db
from app.services.event_service import create_event, get_events, get_event_by_id, update_event, delete_event
from app.schemas.event_schema import EventCreate, EventUpdate, EventResponse

router = APIRouter()

@router.get("/", response_model=list[EventResponse])
def read_events(db: Session = Depends(get_db)):
    events = get_events(db)
    return events

@router.post("/", response_model=EventResponse)
def create_new_event(event: EventCreate, db: Session = Depends(get_db)):
    # TODO: Get current user from JWT token
    created_by = "dummy_user_id"  # Replace with actual user ID from token
    return create_event(db, event, created_by)

@router.get("/{event_id}", response_model=EventResponse)
def read_event(event_id: str, db: Session = Depends(get_db)):
    db_event = get_event_by_id(db, event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

@router.put("/{event_id}", response_model=EventResponse)
def update_existing_event(event_id: str, event: EventUpdate, db: Session = Depends(get_db)):
    db_event = update_event(db, event_id, event)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

@router.delete("/{event_id}")
def delete_existing_event(event_id: str, db: Session = Depends(get_db)):
    db_event = delete_event(db, event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event deleted successfully"}