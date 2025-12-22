from sqlalchemy import Column, Integer, SmallInteger, String
from app.models.base import BaseModel

class SysDict(BaseModel):
    """字典类型表"""

    __tablename__ = "sys_dict"

    code: str = Column(String(50), index=True, comment="类型编码")
    name: str | None = Column(String(50), comment="类型名称")
    status: int = Column(SmallInteger, default=1, comment="状态(0:正常;1:禁用)")
    sort: int = Column(Integer, default=0, comment="排序")


class SysDictItem(BaseModel):
    """字典项表"""

    __tablename__ = "sys_dict_item"

    dict_code: str = Column(String(50), nullable=True)
    value: str | None = Column(String(50))
    label: str | None = Column(String(100))
    tag_type: str | None = Column(String(50))
    status: int = Column(SmallInteger, default=1)
    sort: int = Column(Integer, default=0)
