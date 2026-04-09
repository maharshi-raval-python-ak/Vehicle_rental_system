from pydantic import BaseModel
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

class BookingUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[str] = None
    total_price: Optional[float] = None
