import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, UUID, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.booking_model import Booking
    from app.models.vehicle_checks_model import VehicleCheck
    from app.models.damage_reports_model import DamageReport

class Trip(Base):
    __tablename__ = "trips"
    __table_args__ = {"schema": "backend"}

    trip_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    booking_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("backend.bookings.booking_id"))
    start_time_actual: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    end_time_actual: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    otp_code: Mapped[str] = mapped_column(String(10))
    otp_verified: Mapped[bool] = mapped_column(default=False)
    status: Mapped[str] = mapped_column(String(50))

    booking: Mapped["Booking"] = relationship(back_populates="trip")
    vehicle_checks: Mapped[list["VehicleCheck"]] = relationship(back_populates="trip")
    damage_report: Mapped["DamageReport"] = relationship(back_populates="trip", uselist=False)
