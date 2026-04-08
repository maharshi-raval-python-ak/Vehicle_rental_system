import uuid
from sqlalchemy import UUID, ForeignKey
from app.core.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.roles_model import Role
    from app.models.permissions_model import Permission

class RolePermission(Base):
    __tablename__ = "role_permissions"
    __table_args__ = {"schema": "auth"} 

    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("auth.roles.roles_id", ondelete="CASCADE"), 
        primary_key=True
    )
    permission_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("auth.permissions.permissions_id", ondelete="CASCADE"), 
        primary_key=True
    )
    
    role: Mapped["Role"] = relationship(back_populates="permission_links")
    permission: Mapped["Permission"] = relationship(back_populates="role_links")