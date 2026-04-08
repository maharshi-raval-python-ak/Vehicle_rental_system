import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Text, DateTime, UUID, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.trip_model import Trip

class DamageReport(Base):
    __tablename__ = "damage_reports"
    __table_args__ = {"schema": "backend"}

    report_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("backend.trips.trip_id"))
    description: Mapped[str] = mapped_column(Text)
    extra_charge: Mapped[Optional[float]] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    trip: Mapped["Trip"] = relationship(back_populates="damage_report")
