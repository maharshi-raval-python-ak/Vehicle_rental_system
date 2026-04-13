import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class ReviewBase(BaseModel):
    vehicle_id: uuid.UUID
    rating: int = Field(..., ge=1, le=5, description="Rating must be between 1 and 5 stars, 5 being the best and 1 being the worst.")
    comment: Optional[str] = Field(None, max_length=500)

class ReviewCreate(ReviewBase):
    user_id: uuid.UUID

class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None

class ReviewResponse(ReviewBase):
    review_id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class VehicleReviewSummary(BaseModel):
    average_rating: float
    review_count: int
    reviews: list[ReviewResponse]