import uuid
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.crud.crud_base import CRUDBase
from app.models.vehicle_checks_model import VehicleCheck
from app.schemas.vehicle_checks_schemas import VehicleCheckCreate, VehicleCheckUpdate

class VehicleCheckCRUD(CRUDBase[VehicleCheck, VehicleCheckCreate, VehicleCheckUpdate]):
    
    def get_by_trip(self, db: Session, trip_id: uuid.UUID) -> List[VehicleCheck]:
        query = select(VehicleCheck).where(VehicleCheck.trip_id == trip_id)
        return list(db.execute(query).scalars().all())

vehicle_check_crud = VehicleCheckCRUD(VehicleCheck, "Vehicle Check")
