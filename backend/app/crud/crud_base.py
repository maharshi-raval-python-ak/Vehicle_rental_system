import uuid
from typing import Generic, Type, TypeVar, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException
from pydantic import BaseModel
from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], name: str):
        self.model = model
        self.name = name

    def create(self, obj_in: CreateSchemaType, db: Session) -> ModelType:
        try:
            db_obj = self.model(**obj_in.model_dump())
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"{self.name} already exists.")
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=500, detail="Database error occurred.")

    def get_by_id(self, id: uuid.UUID, db: Session) -> ModelType:
        pk_column = self.model.__mapper__.primary_key[0]
        obj = db.execute(select(self.model).where(pk_column == id)).scalar_one_or_none()
        if not obj:
            raise HTTPException(status_code=404, detail=f"{self.name} not found")
        return obj

    def get_all(self, db: Session) -> List[ModelType]:
        return list(db.execute(select(self.model)).scalars().all())


    def update(self, id: uuid.UUID, obj_in: UpdateSchemaType, db: Session) -> ModelType:
        db_obj = self.get_by_id(id, db)
        update_data = obj_in.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(db_obj, key, value)
            
        try:
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Update conflicts with existing data.")
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=500, detail="Update failed.")

    def delete(self, id: uuid.UUID, db: Session):
        db_obj = self.get_by_id(id, db)
        db.delete(db_obj)
        db.commit()
        return {"detail": f"{self.name} deleted"}
