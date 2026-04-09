import uuid
from typing import List, Set
from pydantic import BaseModel, EmailStr

class AuthData(BaseModel):
    user_id: uuid.UUID
    email: EmailStr
    roles: List[str]
    permissions: Set[str]
    is_valid: str
