from sqlalchemy.orm import Session
from datetime import datetime
from model import models
from schemas import schemas

# User CRUD
def get_user_by_vehicle_number(db: Session, vehicle_number: str):
    return db.query(models.User).filter(models.User.vehicle_number == vehicle_number).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ParkingRecord CRUD
def create_parking_entry(db: Session, user_id: int, entry_time: datetime):
    parking_record = models.ParkingRecord(user_id=user_id, entry_time=entry_time)
    db.add(parking_record)
    db.commit()
    db.refresh(parking_record)
    return parking_record

def update_parking_exit(db: Session, parking_record_id: int, exit_time: datetime):
    parking_record = db.query(models.ParkingRecord).filter(models.ParkingRecord.id == parking_record_id).first()
    if parking_record:
        parking_record.exit_time = exit_time
        db.commit()
        db.refresh(parking_record)
    return parking_record

def get_parking_record_by_user_id(db: Session, user_id: int):
    return db.query(models.ParkingRecord).filter(models.ParkingRecord.user_id == user_id, models.ParkingRecord.exit_time == None).first()
