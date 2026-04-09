from sqlalchemy import select
from sqlalchemy.orm import Session
import uuid
from app.crud.crud_base import CRUDBase
from app.models.trip_model import Trip
from app.schemas.trip_schemas import TripCreate, TripUpdate

class TripCRUD(CRUDBase[Trip, TripCreate, TripUpdate]):
    def get_by_booking(self, booking_id: uuid.UUID, db: Session):
        return db.execute(select(Trip).where(Trip.booking_id == booking_id)).scalar_one_or_none()

trip_crud = TripCRUD(Trip, "Trip")
