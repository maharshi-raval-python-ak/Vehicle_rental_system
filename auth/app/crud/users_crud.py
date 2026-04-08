import uuid
from sqlalchemy.orm import Session
from app.models.users_model import User 

def create(db: Session, email: str, password_hash: str):
    try:
        new_user = User(
            email=email, 
            password_hash=password_hash
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise e

def get_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_by_id(db: Session, user_id: uuid.UUID) -> User | None:
    return db.query(User).filter(User.user_id== user_id).first()