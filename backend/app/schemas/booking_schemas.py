from zoneinfo import ZoneInfo

from pydantic import BaseModel, field_validator
from typing import Optional
import uuid
from datetime import datetime

class BookingBase(BaseModel):
    vehicle_id: uuid.UUID
    start_time: datetime
    end_time: datetime
    total_price: float
    vendor_payout: float
    security_deposit: float

class BookingCreate(BookingBase):
    user_id: uuid.UUID
    otp: str

class BookingUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[str] = None
    total_price: Optional[float] = None

class BookingCreateOuter(BaseModel):
    vehicle_id: uuid.UUID
    start_time: datetime
    end_time: datetime
    
    @field_validator("start_time", "end_time")
    @classmethod
    def ensure_ist(cls, v: datetime):
        ist = ZoneInfo("Asia/Kolkata")
        if v.tzinfo is None:
            return v.replace(tzinfo=ist)
        return v.astimezone(ist)

class BookingResponse(BookingBase):
    booking_id: uuid.UUID
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True