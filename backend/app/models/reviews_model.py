import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Text, DateTime, UUID, ForeignKey, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user_models import User
    from app.models.vehicle_model import Vehicle

class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = {"schema": "backend"}

    review_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("backend.users.user_id"))
    vehicle_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("backend.vehicles.vehicle_id"))
    rating: Mapped[int] = mapped_column(Integer)
    comment: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="reviews")
    vehicle: Mapped["Vehicle"] = relationship(back_populates="reviews")
