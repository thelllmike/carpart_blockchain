from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: str
    vehicle_number: str

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True

class ParkingRecordBase(BaseModel):
    entry_time: Optional[datetime] = None
    exit_time: Optional[datetime] = None

class ParkingRecordCreate(ParkingRecordBase):
    user_id: int

class ParkingRecordOut(ParkingRecordBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
