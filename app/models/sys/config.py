from sqlalchemy import Column, String, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseModel
from app.globals.enum import ConfigTypeEnum



class SysConfig(BaseModel):
    """系统配置表"""

    __tablename__ = "sys_config"

    name: str = Column(String(50), nullable=False)
    key: str = Column(String(50), nullable=False)
    value: str = Column(String(2048), nullable=False)
    type: Mapped[ConfigTypeEnum] = mapped_column(
        SAEnum(ConfigTypeEnum),
        nullable=False,
        default=ConfigTypeEnum.STRING,
        comment="配置类型",
    )
