from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class RoleBase(BaseModel):
    name: str = Field(..., max_length=100, description="Role Name")
    code: str = Field(..., max_length=100, description="Role Code")
    sort: Optional[int] = Field(0, description="Sort Order")
    status: Optional[int] = Field(1, description="Status (1: Normal, 0: Disabled)")
    data_scope: Optional[str] = Field(None, description="Data Scope")
    remark: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    id: int

class RoleResponse(RoleBase):
    id: int
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class DeleteObjsForm(BaseModel):
    ids: List[int]
