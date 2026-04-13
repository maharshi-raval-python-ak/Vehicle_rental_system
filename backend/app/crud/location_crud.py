from app.crud.crud_base import CRUDBase
from app.models.location_model import Location
from app.schemas.location_schemas import LocationCreate, LocationUpdate
from sqlalchemy.orm import Session

class LocationCRUD(CRUDBase[Location, LocationCreate, LocationUpdate]):
    def get_by_area(self, db: Session, area: str) -> Location | None:
        return db.query(Location).filter(Location.area == area).first()

location_crud = LocationCRUD(Location, "Location")

