from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
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

@router.post("/users/", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_vehicle_number(db, vehicle_number=user.vehicle_number)
    if db_user:
        raise HTTPException(status_code=400, detail="Vehicle number already registered")
    return crud.create_user(db, user)
