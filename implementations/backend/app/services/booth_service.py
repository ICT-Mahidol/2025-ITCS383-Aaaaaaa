from sqlalchemy.orm import Session
import uuid
from app.models.booth import Booth
from app.schemas.booth_schema import BoothCreate, BoothUpdate

def create_booth(db: Session, booth: BoothCreate):
    db_booth = Booth(
        booth_id=str(uuid.uuid4()),
        event_id=booth.event_id,
        booth_number=booth.booth_number,
        size=booth.size,
        price=booth.price,
        location=booth.location,
        type=booth.type,
        classification=booth.classification,
        duration_type=booth.duration_type,
        electricity=booth.electricity,
        water_supply=booth.water_supply,
        outlets=booth.outlets
    )
    db.add(db_booth)
    db.commit()
    db.refresh(db_booth)
    return db_booth

def get_booths_by_event(db: Session, event_id: str):
    return db.query(Booth).filter(Booth.event_id == event_id).all()

def get_booth_by_id(db: Session, booth_id: str):
    return db.query(Booth).filter(Booth.booth_id == booth_id).first()

def update_booth(db: Session, booth_id: str, booth: BoothUpdate):
    db_booth = db.query(Booth).filter(Booth.booth_id == booth_id).first()
    if db_booth:
        for key, value in booth.dict(exclude_unset=True).items():
            setattr(db_booth, key, value)
        db.commit()
        db.refresh(db_booth)
    return db_booth

def delete_booth(db: Session, booth_id: str):
    db_booth = db.query(Booth).filter(Booth.booth_id == booth_id).first()
    if db_booth:
        db.delete(db_booth)
        db.commit()
    return db_booth