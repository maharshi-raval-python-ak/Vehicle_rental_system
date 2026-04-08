from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, ForeignKey
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.users_model import User
    from app.models.roles_model import Role

class UsersRole(Base):
    __tablename__ = "users_role"
    __table_args__ = {"schema": "auth"} 

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("auth.users.user_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("auth.roles.roles_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False
    )
    
    user: Mapped["User"] = relationship(back_populates="role_links")
    role: Mapped["Role"] = relationship(back_populates="user_links")