import uuid
from pydantic import BaseModel, ConfigDict

class CreateRole(BaseModel):
    name: str
    description: str
    
class RoleResponse(BaseModel):
    roles_id: uuid.UUID
    name: str
    description: str
    
    model_config = ConfigDict(from_attributes=True)