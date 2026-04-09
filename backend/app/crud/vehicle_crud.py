from sqlalchemy import select
from sqlalchemy.orm import Session
from app.crud.crud_base import CRUDBase
from app.models.vehicle_model import Vehicle
from app.schemas.vehicle_schemas import VehicleCreate, VehicleUpdate

class VehicleCRUD(CRUDBase[Vehicle, VehicleCreate, VehicleUpdate]):
    def get_available_vehicles(self, db: Session):
        return db.execute(select(Vehicle).where(Vehicle.status == "available")).scalars().all()

vehicle_crud = VehicleCRUD(Vehicle, "Vehicle")
