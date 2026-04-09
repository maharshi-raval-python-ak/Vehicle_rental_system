from pydantic import BaseModel
from typing import Optional
import uuid

class ReviewBase(BaseModel):
    vehicle_id: uuid.UUID
    rating: int
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    user_id: uuid.UUID

class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None
