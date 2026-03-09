from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db_connection import get_db
from app.services.booth_service import create_booth, get_booths_by_event, get_booth_by_id, update_booth, delete_booth
from app.schemas.booth_schema import BoothCreate, BoothUpdate, BoothResponse

router = APIRouter()

@router.get("/event/{event_id}", response_model=list[BoothResponse])
def read_booths_by_event(event_id: str, db: Session = Depends(get_db)):
    booths = get_booths_by_event(db, event_id)
    return booths

@router.post("/", response_model=BoothResponse)
def create_new_booth(booth: BoothCreate, db: Session = Depends(get_db)):
    return create_booth(db, booth)

@router.get("/{booth_id}", response_model=BoothResponse)
def read_booth(booth_id: str, db: Session = Depends(get_db)):
    db_booth = get_booth_by_id(db, booth_id)
    if db_booth is None:
        raise HTTPException(status_code=404, detail="Booth not found")
    return db_booth

@router.put("/{booth_id}", response_model=BoothResponse)
def update_existing_booth(booth_id: str, booth: BoothUpdate, db: Session = Depends(get_db)):
    db_booth = update_booth(db, booth_id, booth)
    if db_booth is None:
        raise HTTPException(status_code=404, detail="Booth not found")
    return db_booth

@router.delete("/{booth_id}")
def delete_existing_booth(booth_id: str, db: Session = Depends(get_db)):
    db_booth = delete_booth(db, booth_id)
    if db_booth is None:
        raise HTTPException(status_code=404, detail="Booth not found")
    return {"message": "Booth deleted successfully"}