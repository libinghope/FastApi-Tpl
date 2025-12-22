
from sqlalchemy import Column, String
from app.models.base import BaseModel

class Item(BaseModel):
    __tablename__ = "items"
    title = Column(String(255), index=True)
    description = Column(String(255), index=True)
