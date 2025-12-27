from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.future import select
from sqlalchemy import delete, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models.sys.user import SysUser
from app.models.sys.dictionary import SysDict
from app.schemas.sys.dict import DictCreate, DictUpdate, DictResponse, DeleteObjsForm

router = APIRouter()

@router.get("/list", response_model=dict)
async def list_dicts(
    keywords: Optional[str] = None,
    page_size: int = 10,
    page_number: int = 1,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    stmt = select(SysDict)
    if keywords:
        stmt = stmt.where(
            or_(
                SysDict.code.ilike(f"%{keywords}%"),
                SysDict.name.ilike(f"%{keywords}%"),
            )
        )
    
    # Count
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = await db.scalar(count_stmt)
    
    # Paging
    stmt = stmt.offset((page_number - 1) * page_size).limit(page_size).order_by(SysDict.sort)
    result = await db.execute(stmt)
    dicts = result.scalars().all()
    
    return {"list": [DictResponse.model_validate(d) for d in dicts], "total": total}

@router.post("/add")
async def add_dict(
    form: DictCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    stmt = select(SysDict).where(SysDict.code == form.code)
    if await db.scalar(stmt):
        raise HTTPException(status_code=400, detail="Dict code already exists")
        
    new_dict = SysDict(**form.model_dump())
    db.add(new_dict)
    await db.commit()
    return {"code": 200, "message": "Success"}

@router.post("/update")
async def update_dict(
    form: DictUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    dict_obj = await db.get(SysDict, form.id)
    if not dict_obj:
        raise HTTPException(status_code=404, detail="Dict not found")
        
    for key, value in form.model_dump(exclude={"id"}).items():
        setattr(dict_obj, key, value)
        
    await db.commit()
    return {"code": 200, "message": "Success"}

@router.post("/delete")
async def delete_dict(
    form: DeleteObjsForm,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    await db.execute(delete(SysDict).where(SysDict.id.in_(form.uid_arr)))
    await db.commit()
    return {"code": 200, "message": "Success"}
