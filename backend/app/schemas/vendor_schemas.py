from pydantic import BaseModel, EmailStr
from typing import Optional

class VendorBase(BaseModel):
    name: str
    phone: str

class VendorCreate(VendorBase):
    pass

class VendorUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    is_verified: Optional[bool] = None
    
class VendorResponse(BaseModel):
    name: str
    email: EmailStr
    phone: str
    is_verified: bool
    
    model_config = {"from_attributes": True}
