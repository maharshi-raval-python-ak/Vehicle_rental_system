from sqlalchemy.orm import Session
import uuid
from app.models.role_permissions_model import RolePermission

def create(role_id: uuid.UUID, permission_id: uuid.UUID, db: Session):
    db_object = RolePermission(role_id = role_id, permission_id = permission_id)
    db.add(db_object)
    db.commit()
    db.refresh(db_object)
    return db_object