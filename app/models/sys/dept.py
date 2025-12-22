from sqlalchemy import Column, Index, SmallInteger, String, Integer
from app.models.base import BaseModel

class SysDept(BaseModel):
    """部门表"""

    __tablename__ = "sys_dept"

    name: str = Column(String(100), nullable=False, comment="部门名称")
    code: str = Column(String(100), nullable=False, unique=True, comment="部门编号")
    parent_id: int = Column(
        Integer, nullable=False, default=0, comment="父节点id"
    )
    tree_path: str = Column(String(255), nullable=False, comment="父节点路径")
    sort: int = Column(SmallInteger, default=0, comment="显示顺序")
    status: int = Column(SmallInteger, default=1, comment="状态(1-正常 0-禁用)")

    __table_args__ = (Index("uk_code", "code", unique=True, mysql_length=100),)
