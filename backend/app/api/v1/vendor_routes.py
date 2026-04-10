import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.helpers import authenticated
from app.core.database import get_db
from app.schemas.auth_schemas import AuthData
from app.schemas.response_model import ResponseModel
from app.schemas.vendor_schemas import VendorCreate, VendorResponse
from app.services.vendor_services import vendor_service
from app.schemas.vehicle_schemas import VehicleCreateOuter, VehicleResponse, VehicleUpdate
from app.crud import vehicle_crud
from app.schemas.booking_schemas import BookingResponse
from app.services.booking_services import booking_service

router = APIRouter(prefix="/vendor", tags=["Vendor"])

@router.post("/profile-create", response_model=ResponseModel[dict])
@authenticated(allowed_roles=["vendor"]) 
async def create_vendor_profile(
    access_token: str,
    vendor_in: VendorCreate,
    auth_info: AuthData = Depends(lambda: None),
    db: Session = Depends(get_db),
):
    assert auth_info is not None

    new_vendor = vendor_service.create_vendor_profile(db, vendor_in, auth_info)

    return ResponseModel(
        data={"vendor_id": new_vendor.vendor_id}, 
        message="Vendor profile created successfully"
    )

@router.post("/get/me", response_model=ResponseModel[VendorResponse])
@authenticated(allowed_roles=["vendor"]) 
async def get_vendor_profile(
    access_token: str,
    auth_info: AuthData = Depends(lambda: None),
    db: Session = Depends(get_db),
):
    assert auth_info is not None

    new_vendor = vendor_service.get_vendor_profile(db, auth_info)

    return ResponseModel(
        data=new_vendor, 
        message="Vendor profile retrieved successfully"
    )

@router.post("/vehicle", response_model=ResponseModel[VehicleResponse])
@authenticated(allowed_roles=["vendor"])
async def add_vehicle(
    access_token: str,
    vehicle_in: VehicleCreateOuter,
    db: Session = Depends(get_db),
    auth_info: AuthData = Depends(lambda: None), 
):
    vendor = vendor_service.get_vendor_profile(db, auth_info)

    if not vendor or not vendor.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Vendor account is not verified."
        )

    new_vehicle = vendor_service.create_vehicle_for_vendor(
        db=db, 
        vehicle_in=vehicle_in, 
        vendor_id=auth_info.user_id 
    )

    return {"data": new_vehicle, "message": "Vehicle added successfully"}

@router.get("/vehicles/me", response_model=ResponseModel[list[VehicleResponse]])
@authenticated(allowed_roles=["vendor"])
async def get_my_vehicles(
    access_token: str,
    db: Session = Depends(get_db),
    auth_info: AuthData = Depends(lambda: None),
):
    vehicles = vendor_service.get_my_vehicles(db, auth_info)
    return {"data": vehicles, "message": "Vehicles retrieved successfully"}

@router.patch("/vehicle/{vehicle_id}", response_model=ResponseModel[VehicleResponse])
@authenticated(allowed_roles=["vendor"])
async def update_my_vehicle(
    access_token: str,
    vehicle_id: uuid.UUID,
    vehicle_update: VehicleUpdate,
    db: Session = Depends(get_db),
    auth_info: AuthData = Depends(lambda: None),
):
    updated = vendor_service.update_vendor_vehicle(db, vehicle_id, vehicle_update, auth_info)
    return {"data": updated, "message": "Vehicle updated successfully"}

@router.delete("/vehicle/{vehicle_id}", response_model=ResponseModel[dict])
@authenticated(allowed_roles=["vendor"])
async def delete_my_vehicle(
    access_token: str,
    vehicle_id: uuid.UUID,
    db: Session = Depends(get_db),
    auth_info: AuthData = Depends(lambda: None),
):
    vendor_service.delete_vendor_vehicle(db, vehicle_id, auth_info)
    return {"data": {}, "message": "Vehicle deleted successfully"}

@router.get("/{booking_id}", response_model=ResponseModel[BookingResponse])
@authenticated(allowed_roles=["vendor"])
async def get_booking_for_vendor(
    access_token: str,
    booking_id: uuid.UUID,
    db: Session = Depends(get_db),
    auth_info: AuthData = Depends(lambda: None)
):
    booking = booking_service.get_vendor_booking_detail(db, booking_id, auth_info.user_id)
    return {"data": booking, "message": "Booking details retrieved"}