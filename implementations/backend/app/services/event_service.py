from sqlalchemy.orm import Session
import uuid
from app.models.event import Event
from app.schemas.event_schema import EventCreate, EventUpdate

def create_event(db: Session, event: EventCreate, created_by: str):
    db_event = Event(
        event_id=str(uuid.uuid4()),
        name=event.name,
        description=event.description,
        location=event.location,
        start_date=event.start_date,
        end_date=event.end_date,
        created_by=created_by
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_events(db: Session):
    return db.query(Event).all()

def get_event_by_id(db: Session, event_id: str):
    return db.query(Event).filter(Event.event_id == event_id).first()

def update_event(db: Session, event_id: str, event: EventUpdate):
    db_event = db.query(Event).filter(Event.event_id == event_id).first()
    if db_event:
        for key, value in event.dict(exclude_unset=True).items():
            setattr(db_event, key, value)
        db.commit()
        db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: str):
    db_event = db.query(Event).filter(Event.event_id == event_id).first()
    if db_event:
        db.delete(db_event)
        db.commit()
    return db_event