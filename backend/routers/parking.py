from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from crud import crud
from schemas import schemas
from model.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/parking/entry/")
def record_entry(vehicle_number: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_vehicle_number(db, vehicle_number=vehicle_number)
    if not user:
        raise HTTPException(status_code=404, detail="Vehicle not registered")
    active_parking = crud.get_parking_record_by_user_id(db, user_id=user.id)
    if active_parking:
        raise HTTPException(status_code=400, detail="User already has an active parking session")
    return crud.create_parking_entry(db, user_id=user.id, entry_time=datetime.utcnow())

@router.post("/parking/exit/")
def record_exit(vehicle_number: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_vehicle_number(db, vehicle_number=vehicle_number)
    if not user:
        raise HTTPException(status_code=404, detail="Vehicle not registered")
    active_parking = crud.get_parking_record_by_user_id(db, user_id=user.id)
    if not active_parking:
        raise HTTPException(status_code=400, detail="No active parking session found")
    updated_parking = crud.update_parking_exit(db, parking_record_id=active_parking.id, exit_time=datetime.utcnow())
    parking_duration = (updated_parking.exit_time - updated_parking.entry_time).total_seconds() / 3600
    return {"parking_duration_hours": parking_duration, "user": user.name}
