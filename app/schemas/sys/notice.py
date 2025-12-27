from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class NoticeBase(BaseModel):
    title: Optional[str] = Field(None, max_length=50)
    content: Optional[str] = None
    type: str = Field(..., max_length=50)
    level: str = Field(..., max_length=50)
    target_type: int
    target_user_ids_str: Optional[str] = None
    publisher_id: Optional[int] = None
    publish_status: Optional[int] = Field(0)
    publish_time: Optional[datetime] = None
    revoke_time: Optional[datetime] = None

class NoticeCreate(NoticeBase):
    pass

class NoticeUpdate(NoticeBase):
    id: int

class NoticeResponse(NoticeBase):
    id: int
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
