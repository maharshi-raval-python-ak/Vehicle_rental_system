import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, UUID, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.booking_model import Booking


class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = {"schema": "backend"}

    payment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    booking_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("backend.bookings.booking_id"))
    amount: Mapped[float] = mapped_column(Float)
    payment_type: Mapped[str] = mapped_column(String(20))  # 'booking + deposit' or 'damage'
    method: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(50))
    transaction_id: Mapped[str] = mapped_column(String(100), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    booking: Mapped["Booking"] = relationship(back_populates="payment")
