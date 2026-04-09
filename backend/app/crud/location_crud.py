from app.crud.crud_base import CRUDBase
from app.models.location_model import Location
from app.schemas.location_schemas import LocationCreate, LocationUpdate

class LocationCRUD(CRUDBase[Location, LocationCreate, LocationUpdate]):
    pass

location_crud = LocationCRUD(Location, "Location")
