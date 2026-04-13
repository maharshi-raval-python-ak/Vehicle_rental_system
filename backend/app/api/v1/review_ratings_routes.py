import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.review_services import review_services
from app.schemas.reviews_schemas import ReviewCreate, ReviewResponse, VehicleReviewSummary
from app.utils.helpers import authenticated
from app.schemas.auth_schemas import AuthData

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
@authenticated(allowed_roles=["user"])
async def create_review(
    access_token: str,
    review_in: ReviewCreate, 
    db: Session = Depends(get_db),
    auth_info: AuthData = Depends(lambda: None),
):
    review_in.user_id = auth_info.user_id
    
    return review_services.post_new_review(db=db, review_in=review_in)

@router.get("/vehicle/{vehicle_id}", response_model=VehicleReviewSummary)
@authenticated(allowed_roles=["user", "vendor"])
async def get_vehicle_reviews(access_token: str, vehicle_id: uuid.UUID, db: Session = Depends(get_db), auth_info: AuthData = Depends(lambda: None)):
    return review_services.get_vehicle_summary(db=db, vehicle_id=vehicle_id)

@router.get("/{review_id}", response_model=ReviewResponse)
@authenticated(allowed_roles=["user", "vendor"])
async def get_review(access_token: str, review_id: uuid.UUID, db: Session = Depends(get_db), auth_info: AuthData = Depends(lambda: None)):
    return review_services.get_single_review(db=db, review_id=review_id)

