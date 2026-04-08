from sqlalchemy.orm import Session
from app.models.permissions_model import Permission

def get_by_name(permission_name: str, db: Session):
    return db.query(Permission).filter(Permission.name == permission_name).first()
    
    
    