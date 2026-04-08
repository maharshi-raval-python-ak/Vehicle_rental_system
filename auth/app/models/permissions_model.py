import uuid
from sqlalchemy import UUID, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.role_permissions_model import RolePermission

class Permission(Base):
    __tablename__ = "permissions"
    __table_args__ = {"schema": "auth"} 

    permissions_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    
    role_links: Mapped[list["RolePermission"]] = relationship(back_populates="permission")