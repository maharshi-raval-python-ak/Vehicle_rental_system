from sqlalchemy.orm import Session
from app.crud import vehicle_crud
from app.dao.vehicle_dao import vehicle_dao

class VehicleService:
    def get_all_vehicles(self, db: Session):
        return vehicle_crud.get_all(db)
    
    def get_vehicle_by_vehicle_id(self, db: Session, vehicle_id):
        return vehicle_crud.get_by_id(vehicle_id, db)
    
    def get_filtered_vehicles(self, db, **kwargs):
        return vehicle_dao.search_vehicles(db, **kwargs)
    
vehicle_service = VehicleService()