from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.crud import user_crud
from app.models.user_models import User
from app.schemas.user_schemas import UserCreate
from app.schemas.auth_schemas import AuthData


class UserService:
    def create_profile(self, db: Session, user_in: UserCreate, auth_info: AuthData):
        try:
            user_crud.get_by_id(id=auth_info.user_id, db=db)
            raise HTTPException(status_code=400, detail="Profile already exists")
        except HTTPException as e:
            if e.status_code != 404:
                raise e

        user_data = user_in.model_dump()
        user_data["user_id"] = auth_info.user_id
        user_data["email"] = auth_info.email

        db_obj = User(**user_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_profile(self, db: Session, auth_info: AuthData):
        return user_crud.get_by_id(id=auth_info.user_id, db=db)


user_service = UserService()
