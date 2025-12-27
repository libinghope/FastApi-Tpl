from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class MenuBase(BaseModel):
    parent_id: int = Field(0, description="Parent Menu ID")
    tree_path: Optional[str] = Field(None, max_length=255, description="Tree Path")
    name: str = Field(..., max_length=64, description="Menu Name")
    type: int = Field(..., description="Menu Type")
    route_name: Optional[str] = Field(None, max_length=255)
    route_path: Optional[str] = Field(None, max_length=128)
    component: Optional[str] = Field(None, max_length=128)
    perm: Optional[str] = Field(None, max_length=128)
    always_show: Optional[int] = Field(0)
    keep_alive: Optional[int] = Field(0)
    visible: Optional[bool] = Field(True)
    sort: Optional[int] = Field(0)
    icon: Optional[str] = Field(None, max_length=64)
    redirect: Optional[str] = Field(None, max_length=128)
    params: Optional[str] = Field(None, max_length=1024)

class MenuCreate(MenuBase):
    pass

class MenuUpdate(MenuBase):
    id: int

class MenuResponse(MenuBase):
    id: int
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None
    children: Optional[List['MenuResponse']] = None

    model_config = ConfigDict(from_attributes=True)

class MenuTree(MenuResponse):
    pass
