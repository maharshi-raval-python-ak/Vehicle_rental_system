from sqlalchemy import select
from sqlalchemy.orm import Session
import uuid
from app.crud.crud_base import CRUDBase
from app.models.trip_model import Trip
from app.schemas.trip_schemas import TripCreate, TripUpdate
from app.models.booking_model import Booking

class TripCRUD(CRUDBase[Trip, TripCreate, TripUpdate]):
    def get_by_booking(self, booking_id: uuid.UUID, db: Session):
        return db.execute(select(Trip).where(Trip.booking_id == booking_id)).scalar_one_or_none()
    def get_user_trips(self, db, user_id):
        return db.execute(
            select(Trip).join(Booking).where(Booking.user_id == user_id)
        ).scalars().all()

trip_crud = TripCRUD(Trip, "Trip")
