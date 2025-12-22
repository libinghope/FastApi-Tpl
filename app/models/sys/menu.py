from sqlalchemy import Boolean, Column, Integer, SmallInteger, String
from app.models.base import BaseModel

class SysMenu(BaseModel):
    """菜单表"""

    __tablename__ = "sys_menu"

    parent_id: int = Column(
        Integer, nullable=False, default=0, comment="父菜单ID"
    )
    tree_path: str | None = Column(String(255), comment="父节点ID路径")
    name: str = Column(String(64), nullable=False, comment="菜单名称")
    type: int = Column(SmallInteger, nullable=False, comment="菜单类型")
    route_name: str | None = Column(String(255))
    route_path: str | None = Column(String(128))
    component: str | None = Column(String(128))
    perm: str | None = Column(String(128))
    always_show: int = Column(SmallInteger, default=0)
    keep_alive: int = Column(SmallInteger, default=0)
    visible: bool = Column(Boolean, default=True)
    sort: int = Column(Integer, default=0)
    icon: str | None = Column(String(64))
    redirect: str | None = Column(String(128))
    params: str | None = Column(String(1024))


class SysRoleMenu(BaseModel):
    """角色菜单关联表"""

    __tablename__ = "sys_role_menu"

    role_id: int = Column(Integer, primary_key=True)
    menu_id: int = Column(Integer, primary_key=True)
