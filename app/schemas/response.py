from typing import Generic, TypeVar, Optional, Any, Union
from pydantic import BaseModel

T = TypeVar("T")

class ResponseSchema(BaseModel, Generic[T]):
    code: Union[int, str] = 200
    message: str = "Success"
    data: Optional[T] = None
    
    class Config:
        from_attributes = True

class PageSchema(BaseModel, Generic[T]):
    list: list[T]
    total: int