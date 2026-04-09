import uuid
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name: str
    phone: str
    license_number: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    license_number: Optional[str] = None


class UserRead(BaseModel):
    name: str
    email: EmailStr
    phone: str
    license_number: Optional[str] = None

    model_config = {"from_attributes": True}
