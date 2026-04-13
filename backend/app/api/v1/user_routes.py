import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.helpers import authenticated
from app.core.database import get_db
from app.schemas.auth_schemas import AuthData
from app.schemas.response_model import ResponseModel
from app.schemas.user_schemas import UserCreate, UserRead
from app.services.user_services import user_service
from app.schemas.booking_schemas import (
    BookingCreateOuter,
    BookingResponse,
    BookingUpdate,
)
from app.services.booking_services import booking_service
from app.crud.booking_crud import booking_crud
from app.services.trip_services import trip_service
from app.crud.trip_crud import trip_crud
from app.schemas.trip_schemas import TripResponse

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


@router.post("/", response_model=ResponseModel[BookingResponse])
@authenticated(allowed_roles=["user"])
async def create_new_booking(
    access_token: str,
    booking_in: BookingCreateOuter,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    auth_info: AuthData = Depends(lambda: None),
):
    new_booking = await booking_service.create_booking(
        db=db,
        booking_in=booking_in,
        user_id=auth_info.user_id,
        background_tasks=background_tasks,
        user_email=auth_info.email,
    )

    return {
        "data": new_booking,
        "message": "Booking initiated. OTP sent to your email.",
    }


@router.put("/{booking_id}/cancel", response_model=ResponseModel[BookingResponse])
@authenticated(allowed_roles=["user"])
async def cancel_booking(
    access_token: str,
    booking_id: uuid.UUID,
    db: Session = Depends(get_db),
    auth_info: AuthData = Depends(lambda: None),
):
    update_data = BookingUpdate(status="cancelled")
    updated = booking_crud.update(booking_id, update_data, db)
    return {"data": updated, "message": "Booking cancelled"}


@router.get("/me", response_model=ResponseModel[list[BookingResponse]])
@authenticated(allowed_roles=["user"])
async def get_user_bookings(
    access_token: str,
    db: Session = Depends(get_db),
    auth_info: AuthData = Depends(lambda: None),
):
    bookings = booking_service.get_my_bookings(db, auth_info.user_id)
    return {"data": bookings, "message": "Bookings retrieved"}


#------------------------------------------
#               Trip routes
#------------------------------------------

@router.post("/start", response_model=ResponseModel[TripResponse])
@authenticated(allowed_roles=["user"])
async def start_trip(
    access_token: str,
    booking_id: uuid.UUID,
    otp: str,
    db: Session = Depends(get_db),
    auth_info: AuthData = Depends(lambda: None),
):
    new_trip = trip_service.start_trip(
        db=db, booking_id=booking_id, otp=otp, user_id=auth_info.user_id
    )
    return {"data": new_trip, "message": "OTP Verified. Trip started successfully."}


@router.post("/{trip_id}/end", response_model=ResponseModel[TripResponse])
@authenticated(allowed_roles=["user"])
async def end_trip(
    access_token: str,
    area: str,
    trip_id: uuid.UUID,
    db: Session = Depends(get_db),
    auth_info: AuthData = Depends(lambda: None)
):
    completed_trip = trip_service.end_trip(
        db=db, trip_id=trip_id, user_id=auth_info.user_id, area = area
    )
    return {"data": completed_trip, "message": "Trip completed."}


@router.get("/me", response_model=ResponseModel[list[TripResponse]])
@authenticated(allowed_roles=["user"])
async def get_my_trips(
    access_token: str,
    db: Session = Depends(get_db),
    auth_info: AuthData = Depends(lambda: None),
):
    trips = trip_crud.get_user_trips(db, auth_info.user_id)
    return {"data": trips, "message": "User trips retrieved."}


@router.get("/{trip_id}", response_model=ResponseModel[TripResponse])
@authenticated(allowed_roles=["user", "vendor"])
async def get_trip_details(
    access_token: str,
    trip_id: uuid.UUID,
    db: Session = Depends(get_db),
    auth_info: AuthData = Depends(lambda: None),
):
    trip = trip_crud.get_by_id(trip_id, db)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    is_user = trip.booking.user_id == auth_info.user_id
    is_vendor = trip.booking.vehicle.vendor_id == auth_info.user_id

    if not (is_user or is_vendor):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view this trip.",
        )

    return {"data": trip, "message": "Trip details found."}
