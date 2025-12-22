from sqlalchemy import Column, SmallInteger, String, Boolean, Integer
from typing import ClassVar, List
from app.models.base import BaseModel

class SysUser(BaseModel):
    """用户信息表"""

    __tablename__ = "sys_user"

    username: str | None = Column(String(64), index=True, comment="用户名")
    nickname: str | None = Column(String(64))
    gender: int = Column(SmallInteger, default=1, comment="性别")
    hashed_password: str | None = Column(String(100))
    dept_id: int | None = Column(Integer)
    avatar: str | None = Column(String(255))
    phone_number: str | None = Column(String(20))
    status: int = Column(SmallInteger, default=1)
    email: str | None = Column(String(128))
    openid: str | None = Column(String(28))
    is_superuser: bool = Column(Boolean, default=False, comment="是否超级管理员")
    is_active: bool = Column(Boolean, default=True, comment="是否活动状态")

    # Non-persistent attribute
    roles_id_list: ClassVar[List[str]] = []


class SysUserRoleRef(BaseModel):
    """用户角色关联表"""

    __tablename__ = "user_role_ref"

    user_id: int = Column(
        Integer,
        primary_key=True,
        comment="uid",
    )
    role_id: int = Column(
        Integer,
        primary_key=True,
        comment="uid",
    )
