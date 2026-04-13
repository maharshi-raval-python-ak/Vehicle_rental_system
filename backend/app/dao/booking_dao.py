import uuid
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from app.models.booking_model import Booking
from app.crud.booking_crud import BookingCRUD

class BookingDAO(BookingCRUD):
    def is_vehicle_available(self, db: Session, vehicle_id: uuid.UUID, start_time, end_time) -> bool:
        query = select(Booking).where(
            and_(
                Booking.vehicle_id == vehicle_id,
                Booking.status.in_(["pending", "confirmed"]),
                Booking.start_time < end_time,
                Booking.end_time > start_time
            )
        )
        overlapping = db.execute(query).scalars().first()
        return overlapping is None

booking_dao = BookingDAO(Booking, "Booking")