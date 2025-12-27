from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models.sys.user import SysUser
from app.models.sys.dictionary import SysDictItem
from app.schemas.sys.dict import DictItemCreate, DictItemUpdate, DictItemResponse, DeleteObjsForm

router = APIRouter()

@router.get("/items/{dict_code}/list", response_model=List[DictItemResponse])
async def get_dict_items(
    dict_code: str,
    db: AsyncSession = Depends(deps.get_db),
):
    stmt = select(SysDictItem).where(SysDictItem.dict_code == dict_code).order_by(SysDictItem.sort)
    result = await db.execute(stmt)
    items = result.scalars().all()
    return [DictItemResponse.model_validate(item) for item in items]

@router.post("/items/add")
async def add_dict_item(
    form: DictItemCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    new_item = SysDictItem(**form.model_dump())
    db.add(new_item)
    await db.commit()
    return {"code": 200, "message": "Success"}

@router.post("/items/update")
async def update_dict_item(
    form: DictItemUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    item = await db.get(SysDictItem, form.id)
    if not item:
        raise HTTPException(status_code=404, detail="Dict item not found")
        
    for key, value in form.model_dump(exclude={"id"}).items():
        setattr(item, key, value)
        
    await db.commit()
    return {"code": 200, "message": "Success"}

@router.post("/items/delete")
async def delete_dict_item(
    form: DeleteObjsForm,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    await db.execute(delete(SysDictItem).where(SysDictItem.id.in_(form.uid_arr)))
    await db.commit()
    return {"code": 200, "message": "Success"}
