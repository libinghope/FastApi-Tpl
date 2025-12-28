from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_db
from app.models.item import Item as ItemModel
from app.schemas.item import Item, ItemCreate, ItemUpdate
from app.schemas.response import ResponseSchema, response
from app.core.codes import ErrorCode
from app.core.exceptions import APIException

router = APIRouter()


@router.get("/", response_model=ResponseSchema[List[Item]])
async def read_items(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Retrieve items (Admin).
    """
    result = await db.execute(select(ItemModel).offset(skip).limit(limit))
    items = result.scalars().all()
    return response(data=items)


@router.post("/", response_model=ResponseSchema[Item])
async def create_item(
    *, db: AsyncSession = Depends(get_db), item_in: ItemCreate
) -> Any:
    """
    Create new item (Admin).
    """
    item = ItemModel(title=item_in.title, description=item_in.description)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return response(data=item)


@router.get("/{item_id}", response_model=ResponseSchema[Item])
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)) -> Any:
    """
    Retrieve item (Admin).
    """
    result = await db.execute(select(ItemModel).where(ItemModel.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise APIException(code=ErrorCode.NOT_FOUND, message="Item not found")
    return response(data=item)


@router.put("/{item_id}", response_model=ResponseSchema[Item])
async def update_item(
    item_id: int, item_in: ItemUpdate, db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Update item (Admin).
    """
    result = await db.execute(select(ItemModel).where(ItemModel.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise APIException(code=ErrorCode.NOT_FOUND, message="Item not found")
    item.title = item_in.title
    item.description = item_in.description
    await db.commit()
    await db.refresh(item)
    return response(data=item)


@router.delete("/{item_id}", response_model=ResponseSchema[Item])
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)) -> Any:
    """
    Delete item (Admin).
    """
    result = await db.execute(select(ItemModel).where(ItemModel.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise APIException(code=ErrorCode.NOT_FOUND, message="Item not found")
    await db.delete(item)
    await db.commit()
    return response(data=item)
