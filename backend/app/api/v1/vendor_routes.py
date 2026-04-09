from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.helpers import authenticated
from app.core.database import get_db
from app.schemas.auth_schemas import AuthData
from app.schemas.response_model import ResponseModel
from app.schemas.vendor_schemas import VendorCreate, VendorResponse
from app.services.vendor_services import vendor_service

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
