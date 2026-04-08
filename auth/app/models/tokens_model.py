import uuid
from sqlalchemy import UUID, Boolean, DateTime, ForeignKey, String, func
from app.core.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.users_model import User
    from app.models.clients_model import Client

class Token(Base):
    __tablename__ = "tokens"
    __table_args__ = {"schema": "auth"} 

    token_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("auth.users.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    client_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("auth.clients.client_id", ondelete="CASCADE"),
        nullable=False,
    )
    access_token: Mapped[str] = mapped_column(String, index=True)
    refresh_token: Mapped[str] = mapped_column(String, index=True)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    
    
    user: Mapped["User"] = relationship("User", back_populates="tokens")
    client: Mapped["Client"] = relationship("Client", back_populates="tokens")