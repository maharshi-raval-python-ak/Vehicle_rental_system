from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.helpers import authenticated
from app.core.database import get_db
from app.schemas.auth_schemas import AuthData
from app.schemas.response_model import ResponseModel
from app.schemas.user_schemas import UserCreate, UserRead
from app.services.user_services import user_service

router = APIRouter(prefix="/user", tags=["User Profile"])


@router.post("/profile-create", response_model=ResponseModel[dict])
@authenticated(allowed_roles=["user"])
async def create_user_profile(
    access_token: str,
    user_in: UserCreate,
    auth_info: AuthData = Depends(lambda: None),
    db: Session = Depends(get_db),
):
    assert auth_info is not None

    new_user = user_service.create_profile(db, user_in, auth_info)

    return ResponseModel(
        data={"user_id": new_user.user_id}, message="Profile created successfully"
    )


@router.get("/profile/me", response_model=ResponseModel[UserRead])
@authenticated(allowed_roles=["user"])
async def get_user_profile(
    access_token: str,
    auth_info: AuthData = Depends(lambda: None),
    db: Session = Depends(get_db),
):
    assert auth_info is not None

    profile = user_service.get_profile(db, auth_info)

    return ResponseModel(data=profile, message="Profile retrieved successfully")
