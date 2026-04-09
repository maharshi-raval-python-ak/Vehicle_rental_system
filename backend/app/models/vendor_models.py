import uuid
from datetime import datetime
from typing import List
from sqlalchemy import String, DateTime, UUID, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.vehicle_model import Vehicle

class Vendor(Base):
    __tablename__ = "vendors"
    __table_args__ = {"schema": "backend"}

    vendor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(15))
    is_verified: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


    vehicles: Mapped[List["Vehicle"]] = relationship(back_populates="vendor")
