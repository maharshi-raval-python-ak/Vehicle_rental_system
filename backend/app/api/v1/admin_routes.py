import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.helpers import authenticated
from app.core.database import get_db
from app.schemas.auth_schemas import AuthData
from app.schemas.response_model import ResponseModel
from app.services.admin_services import admin_service
from app.schemas.vendor_schemas import VendorResponse

router = APIRouter(prefix="/admin", tags=["Admin Operations"])


@router.patch("/verify-vendor/{vendor_id}", response_model=ResponseModel[dict])
@authenticated(allowed_roles=["admin"])
async def verify_vendor(
    access_token: str,
    vendor_id: uuid.UUID,
    is_verified: bool,
    db: Session = Depends(get_db),
    auth_info: AuthData = Depends(lambda: None),
):
    assert auth_info is not None

    vendor = admin_service.verify_vendor(db, vendor_id, is_verified)

    status_text = "verified" if vendor.is_verified else "unverified"
    return ResponseModel(
        data={"vendor_id": vendor.vendor_id, "status": status_text},
        message=f"Vendor successfully {status_text}",
    )


@router.get("/get-vendors", response_model=ResponseModel[list[VendorResponse]])
@authenticated(allowed_roles=["admin"])
async def get_vendors(
    access_token: str,
    db: Session = Depends(get_db),
    auth_info: AuthData = Depends(lambda: None),
):
    assert auth_info is not None

    vendors = admin_service.get_vendors(db)

    return ResponseModel(data=vendors, message=f"Vendor successfully retrieved")
