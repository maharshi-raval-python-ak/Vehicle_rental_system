import uuid
from sqlalchemy.orm import Session
from app.crud.vendor_crud import vendor_crud

class AdminService:
    def verify_vendor(self, db: Session, vendor_id: uuid.UUID, is_verified: bool):
        vendor = vendor_crud.get_by_id(id=vendor_id, db=db)        
        vendor.is_verified = is_verified
        db.commit()
        db.refresh(vendor)
        return vendor
    
    def get_vendors(self, db: Session):
        vendors = vendor_crud.get_all(db)
        return vendors

admin_service = AdminService()
