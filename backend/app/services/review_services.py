import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.dao.review_dao import review_dao
from app.crud.reviews_crud import review_crud
from app.schemas.reviews_schemas import ReviewCreate

class ReviewService:
    @staticmethod
    def post_new_review(db: Session, review_in: ReviewCreate):
        if not review_dao.has_completed_trip(db, review_in.user_id, review_in.vehicle_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only review vehicles after completing a trip."
            )

        if review_dao.already_reviewed(db, review_in.user_id, review_in.vehicle_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already reviewed this vehicle."
            )

        return review_crud.create(obj_in=review_in, db=db)
    
    def get_vehicle_summary(self, db: Session, vehicle_id: uuid.UUID):
        reviews = review_crud.get_multi_by_vehicle(db=db, vehicle_id=vehicle_id)
        
        count = len(reviews)
        avg_rating = sum(r.rating for r in reviews) / count if count > 0 else 0.0
        
        return {
            "average_rating": round(avg_rating, 2),
            "review_count": count,
            "reviews": reviews
        }

    def get_single_review(self, db: Session, review_id: uuid.UUID):
        return review_crud.get_by_id(db=db, id=review_id)
    
    
review_services = ReviewService()