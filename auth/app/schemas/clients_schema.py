from datetime import datetime
from pydantic import BaseModel, ConfigDict, HttpUrl, field_validator
import uuid

class ClientCreate(BaseModel):
    client_name: str
    redirect_url: HttpUrl
    
    @field_validator("redirect_url", mode="after")
    @classmethod
    def url_to_string(cls, v):
        return str(v)
    
class ClientResponse(BaseModel):
    client_id: uuid.UUID
    client_name: str
    redirect_url: str
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)