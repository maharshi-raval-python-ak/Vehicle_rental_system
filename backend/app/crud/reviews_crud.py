import uuid
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.crud.crud_base import CRUDBase
from app.models.reviews_model import Review
from app.schemas.reviews_schemas import ReviewCreate, ReviewUpdate

class ReviewCRUD(CRUDBase[Review, ReviewCreate, ReviewUpdate]):
    def get_multi_by_vehicle(self, db: Session, vehicle_id: uuid.UUID) -> List[Review]:
        return list(db.execute(select(Review).where(Review.vehicle_id == vehicle_id)).scalars().all())

review_crud = ReviewCRUD(Review, "Review")
