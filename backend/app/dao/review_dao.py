import uuid
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from app.models.booking_model import Booking
from app.models.reviews_model import Review
from app.crud.reviews_crud import ReviewCRUD

class ReviewDAO(ReviewCRUD):
    def has_completed_trip(self, db: Session, user_id: uuid.UUID, vehicle_id: uuid.UUID) -> bool:
        query = select(Booking).where(
            and_(
                Booking.user_id == user_id,
                Booking.vehicle_id == vehicle_id,
                Booking.status == "completed"
            )
        )
        return db.execute(query).scalars().first() is not None

    def already_reviewed(self, db: Session, user_id: uuid.UUID, vehicle_id: uuid.UUID) -> bool:
        query = select(Review).where(
            and_(
                Review.user_id == user_id,
                Review.vehicle_id == vehicle_id
            )
        )
        return db.execute(query).scalars().first() is not None
    
review_dao = ReviewDAO(Review, "Review")