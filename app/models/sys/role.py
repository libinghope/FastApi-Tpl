from typing import Any


from sqlalchemy import (
    Column,
    Integer,
    SmallInteger,
    String,
    Enum,
)
from app.models.base import BaseModel
from app.globals.enum import RoleDataScope


class SysRole(BaseModel):
    """角色表"""

    __tablename__ = "sys_role"

    name: str = Column(String(100), nullable=False, comment="角色名称")
    code: str = Column(String(100), nullable=False, comment="角色编码")
    sort: int | None = Column(Integer)
    status: int = Column(SmallInteger, default=1, comment="角色状态")
    data_scope: RoleDataScope = Column[Enum](
        Enum(RoleDataScope), default=RoleDataScope.ALL, comment="数据范围"
    )
