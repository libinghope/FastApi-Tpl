from sqlalchemy import (
    BigInteger,
    SmallInteger,
    Column,
    String,
    Text,
    Integer
)
from app.models.base import BaseModel

class SysLog(BaseModel):
    __tablename__ = "sys_log"

    user_id: int = Column(Integer, nullable=True, default=-1, comment="用户id")
    module: str = Column(String(50), nullable=True)
    request_method: str = Column(String(64), nullable=False)
    request_params: str | None = Column(Text)
    response_content: str | None = Column(Text)
    content: str = Column(Text, nullable=False, comment="日志内容")
    request_uri: str | None = Column(String(255))
    method: str | None = Column(String(255))
    ip: str | None = Column(String(45))
    province: str | None = Column(String(100))
    city: str | None = Column(String(100))
    execution_time: int | None = Column(BigInteger)
    browser: str | None = Column(String(100))
    browser_version: str | None = Column(String(100))
    os: str | None = Column(String(100))
    status_code: int | None = Column(SmallInteger)
