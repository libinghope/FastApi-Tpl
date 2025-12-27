from typing import Optional, List
from pydantic import BaseModel, Field

class DictBase(BaseModel):
    code: str = Field(..., description="Type Code")
    name: Optional[str] = Field(None, description="Type Name")
    status: int = Field(1, description="Status (1: Normal, 0: Disabled)")
    sort: int = Field(0, description="Sort Order")

class DictCreate(DictBase):
    pass

class DictUpdate(DictBase):
    id: int

class DictResponse(DictBase):
    id: int

    class Config:
        from_attributes = True

class DictItemBase(BaseModel):
    dict_code: str = Field(..., description="Dict Type Code")
    label: str = Field(..., description="Label")
    value: str = Field(..., description="Value")
    tag_type: Optional[str] = Field(None, description="Tag Type (success, info, warning, danger)")
    status: int = Field(1, description="Status (1: Normal, 0: Disabled)")
    sort: int = Field(0, description="Sort Order")

class DictItemCreate(DictItemBase):
    pass

class DictItemUpdate(DictItemBase):
    id: int

class DictItemResponse(DictItemBase):
    id: int

    class Config:
        from_attributes = True

class DeleteObjsForm(BaseModel):
    uid_arr: List[int] = Field(..., description="List of IDs to delete")
