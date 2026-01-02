from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    SmallInteger,
    String,
    Text,
    Integer,
    UniqueConstraint,
)
from app.models.base import BaseModel


class SysNotice(BaseModel):
    """通知公告表"""

    __tablename__ = "sys_notice"

    title: str | None = Column(String(50))
    content: str | None = Column(Text)
    type: str = Column(String(50), nullable=False)
    level: str = Column(String(50), nullable=False)
    target_type: int = Column(SmallInteger, nullable=False)
    target_user_ids_str: str | None = Column(Text)
    publisher_id: int | None = Column(Integer)
    publish_status: int = Column(SmallInteger, default=0)
    publish_time: datetime | None = Column(DateTime)
    revoke_time: datetime | None = Column(DateTime)


class SysUserNotice(BaseModel):
    """用户通知公告表"""

    __tablename__ = "sys_user_notice"

    notice_id: int = Column(Integer, nullable=False)
    user_id: int = Column(Integer, nullable=False)
    is_read: bool = Column(Boolean, default=False)
    read_time: datetime | None = Column(DateTime)

    __table_args__ = (UniqueConstraint("notice_id", "user_id"),)
