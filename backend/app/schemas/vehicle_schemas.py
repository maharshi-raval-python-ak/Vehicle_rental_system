from pydantic import BaseModel
from typing import Optional
import uuid

class VehicleBase(BaseModel):
    type: str
    brand: str
    model_name: str
    fuel_type: str
    seating_capacity: int
    price_per_hour: float
    deposit_amount: float
    location_id: uuid.UUID

class VehicleCreate(VehicleBase):
    vendor_id: uuid.UUID

class VehicleUpdate(BaseModel):
    type: Optional[str] = None
    brand: Optional[str] = None
    model_name: Optional[str] = None
    seating_capacity: Optional[int] = None
    price_per_hour: Optional[float] = None
    status: Optional[str] = None
