from sqlalchemy import select
from sqlalchemy.orm import Session
from app.crud.crud_base import CRUDBase
from app.models.user_models import User
from app.schemas.user_schemas import UserCreate, UserUpdate

class UserCRUD(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, email: str, db: Session):
        return db.execute(select(User).where(User.email == email)).scalar_one_or_none()

user_crud = UserCRUD(User, "User")
