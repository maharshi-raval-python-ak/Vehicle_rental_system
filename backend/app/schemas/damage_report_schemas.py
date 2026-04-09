from pydantic import BaseModel
from typing import Optional
import uuid

class DamageReportBase(BaseModel):
    trip_id: uuid.UUID
    description: str
    extra_charge: Optional[float] = 0.0

class DamageReportCreate(DamageReportBase):
    pass

class DamageReportUpdate(BaseModel):
    description: Optional[str] = None
    extra_charge: Optional[float] = None
