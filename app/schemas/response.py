from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel

T = TypeVar("T")

class ResponseSchema(BaseModel, Generic[T]):
    code: int = 200
    message: str = "Success"
    data: Optional[T] = None
    
    class Config:
        from_attributes = True

class PageSchema(BaseModel, Generic[T]):
    list: list[T]
    total: int
