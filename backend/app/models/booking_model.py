import uuid
from datetime import datetime
from sqlalchemy import String, Float, UUID, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user_models import User
    from app.models.vehicle_model import Vehicle
    from app.models.trip_model import Trip
    from app.models.payments_model import Payment

class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = {"schema": "backend"}

    booking_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("backend.users.user_id"))
    vehicle_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("backend.vehicles.vehicle_id"))
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    
    total_price: Mapped[float] = mapped_column(Float)
    vendor_payout: Mapped[float] = mapped_column(Float)
    security_deposit: Mapped[float] = mapped_column(Float)
    
    status: Mapped[str] = mapped_column(String(50), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


    user: Mapped["User"] = relationship(back_populates="bookings")
    vehicle: Mapped["Vehicle"] = relationship(back_populates="bookings")
    trip: Mapped["Trip"] = relationship(back_populates="booking", uselist=False)
    payment: Mapped[list["Payment"]] = relationship(back_populates="booking")
