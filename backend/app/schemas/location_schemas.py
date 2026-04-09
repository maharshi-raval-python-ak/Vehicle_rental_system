from pydantic import BaseModel
from typing import Optional

class LocationBase(BaseModel):
    city: str
    area: str
    latitude: float
    longitude: float

class LocationCreate(LocationBase):
    pass

class LocationUpdate(BaseModel):
    city: Optional[str] = None
    area: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
