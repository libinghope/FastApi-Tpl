from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.item import Item as ItemModel
from app.schemas.item import Item
from app.api.deps import get_db
from app.schemas.response import ResponseSchema, response

router = APIRouter()


@router.get("/", response_model=ResponseSchema[List[Item]])
async def read_items(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Retrieve items (Public).
    """
    result = await db.execute(select(ItemModel).offset(skip).limit(limit))
    items = result.scalars().all()
    return response(data=items)
