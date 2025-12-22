from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Integer,
    SmallInteger,
    String,
    UniqueConstraint,
)
from app.models.base import BaseModel

class GenConfig(BaseModel):
    """代码生成基础配置表"""

    __tablename__ = "gen_config"

    table_name: str = Column(String(100), nullable=False)
    module_name: str | None = Column(String(100))
    package_name: str = Column(String(255), nullable=False)
    business_name: str = Column(String(100), nullable=False)
    entity_name: str = Column(String(100), nullable=False)
    author: str = Column(String(50), nullable=False)
    parent_menu_id: int | None = Column(Integer)  # Changed from BigInteger to Integer to match menu_id type usually

    __table_args__ = (UniqueConstraint("table_name", name="uk_tablename"),)


class GenFieldConfig(BaseModel):
    """代码生成字段配置表"""

    __tablename__ = "gen_field_config"

    config_id: int = Column(Integer, nullable=False, default=-1) # Should this be FK? Or just linkage?
    column_name: str | None = Column(String(100))
    column_type: str | None = Column(String(50))
    column_length: int | None = Column(Integer)
    field_name: str = Column(String(100), nullable=False)
    field_type: str | None = Column(String(100))
    field_sort: int | None = Column(Integer)
    field_comment: str | None = Column(String(255))
    max_length: int | None = Column(Integer)
    is_required: bool | None = Column(Boolean)
    is_show_in_list: bool = Column(Boolean, default=False)
    is_show_in_form: bool = Column(Boolean, default=False)
    is_show_in_query: bool = Column(Boolean, default=False)
    query_type: int | None = Column(SmallInteger)
    form_type: int | None = Column(SmallInteger)
    dict_type: str | None = Column(String(50))
