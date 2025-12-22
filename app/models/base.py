from sqlalchemy import Column, DateTime, String, Integer, func
from app.db.base import Base

class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    create_time = Column(DateTime, default=func.now(), comment="创建时间")
    update_time = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    delete_time = Column(DateTime, nullable=True, comment="删除时间")
    create_by = Column(String(255), nullable=True, comment="创建者")
    update_by = Column(String(255), nullable=True, comment="更新者")
    delete_by = Column(String(255), nullable=True, comment="删除者")
    remark = Column(String(255), nullable=True, comment="备注")
