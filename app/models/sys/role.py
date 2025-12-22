from sqlalchemy import (
    Column,
    Integer,
    SmallInteger,
    String,
)
from app.models.base import BaseModel

class SysRole(BaseModel):
    """角色表"""

    __tablename__ = "sys_role"

    name: str = Column(String(100), nullable=False, comment="角色名称")
    code: str = Column(String(100), nullable=False, comment="角色编码")
    sort: int | None = Column(Integer)
    status: int = Column(SmallInteger, default=1, comment="角色状态")
    data_scope: int | None = Column(SmallInteger)
