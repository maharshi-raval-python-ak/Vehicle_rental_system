import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.roles_schema import CreateRole
from app.crud import roles_crud
from app.crud import users_role_crud
from app.crud import permissions_crud
from app.crud import role_permissions_crud

def create_role_service(role_data: CreateRole, db: Session):
    return roles_crud.create(role_data, db)

def assign_role_to_users_service(user_id: uuid.UUID, role_name: str, db: Session):
    db_role = roles_crud.get_by_name(role_name, db)
    if db_role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found.")
    role_id = db_role.roles_id
    return users_role_crud.create(user_id, role_id, db)

def add_permissions_to_role_service(role_id: uuid.UUID, permission_name: str, db: Session):
    db_permission = permissions_crud.get_by_name(permission_name, db)
    if db_permission is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found.")
    permission_id = db_permission.permissions_id
    return role_permissions_crud.create(role_id, permission_id, db)
    
    
    