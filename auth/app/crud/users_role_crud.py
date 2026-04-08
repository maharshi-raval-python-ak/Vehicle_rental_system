import uuid
from sqlalchemy.orm import Session
from app.models.users_role_model import UsersRole

def create(user_id: uuid.UUID, role_id: uuid.UUID, db: Session):
    db_object = UsersRole(user_id = user_id, role_id = role_id)
    db.add(db_object)
    db.commit()
    db.refresh(db_object)
    return db_object