from typing import Optional
from pydantic import BaseModel, Field
from app.models.sys.config import ConfigTypeEnum
from datetime import datetime

class ConfigBase(BaseModel):
    name: str = Field(..., max_length=50, description="Config Name")
    key: str = Field(..., max_length=50, description="Config Key")
    value: str = Field(..., max_length=2048, description="Config Value")
    type: ConfigTypeEnum = Field(default=ConfigTypeEnum.STRING, description="Config Type")
    remark: Optional[str] = Field(None, max_length=255, description="Remark")

class ConfigCreate(ConfigBase):
    pass

class ConfigUpdate(ConfigBase):
    id: int = Field(..., description="Config ID")

class ConfigResponse(ConfigBase):
    id: int
    create_time: datetime
    update_time: datetime

    class Config:
        from_attributes = True

class ConfigFilter(BaseModel):
    keywords: Optional[str] = None
    page_size: int = 10
    page_number: int = 1
