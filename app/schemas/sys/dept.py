from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

class DeptBase(BaseModel):
    name: str = Field(..., description="Department Name")
    code: str = Field(..., description="Department Code")
    parent_id: int = Field(0, description="Parent Department ID")
    sort: int = Field(0, description="Sort Order")
    status: int = Field(1, description="Status (1: Normal, 0: Disabled)")
    remark: Optional[str] = None

class DeptCreate(DeptBase):
    pass

class DeptUpdate(DeptBase):
    id: int

class DeptResponse(DeptBase):
    id: int
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None
    children: Optional[List['DeptResponse']] = None

    class Config:
        from_attributes = True

class DeptTree(DeptResponse):
    pass

class DeleteObjsForm(BaseModel):
    ids: List[int]
