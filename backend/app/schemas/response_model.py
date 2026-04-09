from typing import Generic, TypeVar
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class ResponseModel(BaseModel, Generic[T]):
    status: str = "success"
    data: T
    message: str

    model_config = ConfigDict(from_attributes=True)
