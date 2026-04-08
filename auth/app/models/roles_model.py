from sqlalchemy import UUID, String
from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.users_role_model import UsersRole
    from app.models.role_permissions_model import RolePermission

class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {"schema": "auth"} 
    
    roles_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String)
    
    user_links: Mapped[list["UsersRole"]] = relationship(back_populates="role")
    permission_links: Mapped[list["RolePermission"]] = relationship(back_populates="role")