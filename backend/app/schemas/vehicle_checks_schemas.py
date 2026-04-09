from pydantic import BaseModel
from typing import Optional
import uuid

class VehicleCheckBase(BaseModel):
    trip_id: uuid.UUID
    image_url: str
    type: str # 'before' or 'after'
    uploaded_by: str # 'user' or 'vendor'

class VehicleCheckCreate(VehicleCheckBase):
    pass

class VehicleCheckUpdate(BaseModel):
    image_url: Optional[str] = None
