from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class TripBase(BaseModel):
    booking_id: uuid.UUID
    status: str

class TripCreate(TripBase):
    otp_code: str

class TripUpdate(BaseModel):
    start_time_actual: Optional[datetime] = None
    end_time_actual: Optional[datetime] = None
    otp_verified: Optional[bool] = None
    status: Optional[str] = None
