from sqlalchemy import select
from sqlalchemy.orm import Session
from app.crud.crud_base import CRUDBase
from app.models.vendor_models import Vendor
from app.schemas.vendor_schemas import VendorCreate, VendorUpdate

class VendorCRUD(CRUDBase[Vendor, VendorCreate, VendorUpdate]):
    def get_by_email(self, email: str, db: Session):
        return db.execute(select(Vendor).where(Vendor.email == email)).scalar_one_or_none()

vendor_crud = VendorCRUD(Vendor, "Vendor")
