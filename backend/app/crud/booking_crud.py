from sqlalchemy import select
from sqlalchemy.orm import Session
import uuid
from app.crud.crud_base import CRUDBase
from app.models.booking_model import Booking
from app.schemas.booking_schemas import BookingCreate, BookingUpdate

class BookingCRUD(CRUDBase[Booking, BookingCreate, BookingUpdate]):
    def get_by_user(self, user_id: uuid.UUID, db: Session):
        return db.execute(select(Booking).where(Booking.user_id == user_id)).scalars().all()

booking_crud = BookingCRUD(Booking, "Booking")
