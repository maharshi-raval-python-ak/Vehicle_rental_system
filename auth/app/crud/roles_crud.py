from fastapi import HTTPException

from app.schemas.roles_schema import CreateRole
from sqlalchemy.orm import Session
from app.models.roles_model import Role

def create(role_data: CreateRole, db: Session):
    existing= db.query(Role).filter(Role.name == role_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Role already registered.")
    
    db_role = Role(name = role_data.name,
                   description = role_data.description)
    
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def get_by_name(role_name: str, db: Session):
    return db.query(Role).filter(Role.name == role_name).first()