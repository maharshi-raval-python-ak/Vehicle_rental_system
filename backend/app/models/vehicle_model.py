import uuid
from typing import List 
from sqlalchemy import String, Float, UUID, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.vendor_models import Vendor
    from app.models.location_model import Location
    from app.models.booking_model import Booking
    from app.models.reviews_model import Review

class Vehicle(Base):
    __tablename__ = "vehicles"
    __table_args__ = {"schema": "backend"}

    vehicle_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    vendor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("backend.vendors.vendor_id"))
    location_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("backend.locations.location_id"))
    type: Mapped[str] = mapped_column(String(50))
    brand: Mapped[str] = mapped_column(String(50))
    model_name: Mapped[str] = mapped_column(String(100))
    fuel_type: Mapped[str] = mapped_column(String(50))
    seating_capacity: Mapped[int] = mapped_column(Integer)
    price_per_hour: Mapped[float] = mapped_column(Float)
    deposit_amount: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(50), default="available")

    vendor: Mapped["Vendor"] = relationship(back_populates="vehicles")
    location: Mapped["Location"] = relationship(back_populates="vehicles")
    bookings: Mapped[List["Booking"]] = relationship(back_populates="vehicle")
    reviews: Mapped[List["Review"]] = relationship(back_populates="vehicle") 
