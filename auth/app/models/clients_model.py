from datetime import datetime
from sqlalchemy import UUID, String, Boolean, DateTime, func
from app.core.database import Base
import uuid
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.tokens_model import Token

class Client(Base):
    __tablename__ = "clients"
    __table_args__ = {"schema": "auth"} 

    client_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    client_name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    client_secret: Mapped[str] = mapped_column(String, nullable=False)
    redirect_url: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


    tokens: Mapped[list["Token"]] = relationship("Token", back_populates="client")
