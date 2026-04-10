from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class TripBase(BaseModel):
    booking_id: uuid.UUID
    status: str

class TripCreate(TripBase):
   pass

class TripUpdate(BaseModel):
    start_time_actual: Optional[datetime] = None
    end_time_actual: Optional[datetime] = None
    otp_verified: Optional[bool] = None
    status: Optional[str] = None

class TripResponse(BaseModel):
    trip_id: uuid.UUID
    booking_id: uuid.UUID
    status: str
    start_time_actual: Optional[datetime]
    end_time_actual: Optional[datetime]

    model_config = {"from_attributes": True}
