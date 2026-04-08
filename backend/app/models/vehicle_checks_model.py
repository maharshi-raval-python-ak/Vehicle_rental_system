import uuid
from datetime import datetime
from sqlalchemy import String, Text, DateTime, UUID, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.trip_model import Trip

class VehicleCheck(Base):
    __tablename__ = "vehicle_checks"
    __table_args__ = {"schema": "backend"}

    check_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("backend.trips.trip_id"))
    image_url: Mapped[str] = mapped_column(Text)
    type: Mapped[str] = mapped_column(String(20)) # 'before' or 'after'
    uploaded_by: Mapped[str] = mapped_column(String(20)) # 'user' or 'vendor'
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    trip: Mapped["Trip"] = relationship(back_populates="vehicle_checks")
