from datetime import datetime
import uuid
from pydantic import BaseModel, ConfigDict, EmailStr

class UserRegister(BaseModel):
    email: EmailStr  
    password: str 
    
    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    user_id: uuid.UUID
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
