import uuid
from sqlalchemy import String, Float, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.vehicle_model import Vehicle

class Location(Base):
    __tablename__ = "locations"
    __table_args__ = {"schema": "backend"}

    location_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    city: Mapped[str] = mapped_column(String(100))
    area: Mapped[str] = mapped_column(String(100))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)

    vehicles: Mapped[list["Vehicle"]] = relationship(back_populates="location")
