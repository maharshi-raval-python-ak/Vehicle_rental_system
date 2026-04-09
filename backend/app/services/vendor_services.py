from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.crud.vendor_crud import vendor_crud
from app.models.vendor_models import Vendor
from app.schemas.vendor_schemas import VendorCreate
from app.schemas.auth_schemas import AuthData

class VendorService:
    def create_vendor_profile(self, db: Session, vendor_in: VendorCreate, auth_info: AuthData):
        try:
            vendor_crud.get_by_id(id=auth_info.user_id, db=db)
            raise HTTPException(status_code=400, detail="Vendor profile already exists")
        except HTTPException as e:
            if e.status_code != 404:
                raise e

        vendor_data = vendor_in.model_dump()
        vendor_data["vendor_id"] = auth_info.user_id 
        vendor_data["email"] = auth_info.email

        db_obj = Vendor(**vendor_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_vendor_profile(self, db: Session, auth_info: AuthData):
        return vendor_crud.get_by_id(id=auth_info.user_id, db=db)
    
vendor_service = VendorService()
