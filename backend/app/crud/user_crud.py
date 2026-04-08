from app.models.user_models import User
from app.schemas.user_schemas import UserCreate, UserUpdate
from app.crud.base import CRUDBase

class UserCRUD(CRUDBase[User, UserCreate, UserUpdate]):
    # You can add custom methods here like get_by_email
    def get_by_email(self, email: str, db: Session):
        return db.execute(select(User).where(User.email == email)).scalar_one_or_none()

user_crud = UserCRUD(User, "User")
