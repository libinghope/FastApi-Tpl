from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func

from app.api import deps
from app.models.sys.config import SysConfig
from app.models.sys.user import SysUser
from app.schemas.sys.config import ConfigCreate, ConfigUpdate, ConfigResponse
from app.schemas.response import ResponseSchema, PageSchema
from app.core.codes import ErrorCode

router = APIRouter()


@router.get("/list", response_model=ResponseSchema[PageSchema[ConfigResponse]])
async def get_config_list(
    keywords: Optional[str] = None,
    page_size: int = 10,
    page_number: int = 1,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    stmt = (
        select(SysConfig).where(SysConfig.is_deleted == False)
        if hasattr(SysConfig, "is_deleted")
        else select(SysConfig)
    )

    # Check if is_deleted exists in BaseModel or SysConfig.
    # BaseModel (step 21) has delete_time, not is_deleted.
    # Usually is_deleted is a computed property or we check delete_time is None.
    # Let's check BaseModel again.
    # BaseModel has delete_time. So we should check delete_time is None.
    stmt = select(SysConfig).where(SysConfig.delete_time == None)

    if keywords:
        stmt = stmt.where(
            or_(
                SysConfig.name.ilike(f"%{keywords}%"),
                SysConfig.key.ilike(f"%{keywords}%"),
            )
        )

    # Count
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = await db.scalar(count_stmt)

    # Paging
    stmt = stmt.offset((page_number - 1) * page_size).limit(page_size)
    result = await db.execute(stmt)
    configs = result.scalars().all()

    return ResponseSchema(
        result=PageSchema(
            list=[ConfigResponse.model_validate(c) for c in configs], total=total
        )
    )


@router.post("/add", response_model=ResponseSchema[ConfigResponse])
async def add_config(
    form: ConfigCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    # Check duplicates
    stmt = select(SysConfig).where(
        or_(SysConfig.key == form.key, SysConfig.name == form.name),
        SysConfig.delete_time == None,
    )
    result = await db.execute(stmt)
    existing = result.scalars().first()
    if existing:
        if existing.key == form.key:
            return ResponseSchema(
                code=ErrorCode.CONFIG_KEY_EXISTS, message="Config Key already exists"
            )
        if existing.name == form.name:
            return ResponseSchema(
                code=ErrorCode.CONFIG_NAME_EXISTS, message="Config Name already exists"
            )

    new_config = SysConfig(
        name=form.name,
        key=form.key,
        value=form.value,
        type=form.type,
        remark=form.remark,
        create_by=current_user.username,
    )
    db.add(new_config)
    await db.commit()
    await db.refresh(new_config)
    return ResponseSchema(result=new_config)


@router.post("/update", response_model=ResponseSchema[ConfigResponse])
async def update_config(
    form: ConfigUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    config = await db.get(SysConfig, form.id)
    if not config or config.delete_time is not None:
        return ResponseSchema(
            code=ErrorCode.CONFIG_NOT_FOUND, message="Config not found"
        )

    # Check duplicates if key/name changed
    stmt = select(SysConfig).where(
        or_(SysConfig.key == form.key, SysConfig.name == form.name),
        SysConfig.id != form.id,
        SysConfig.delete_time == None,
    )
    result = await db.execute(stmt)
    existing = result.scalars().first()
    if existing:
        if existing.key == form.key:
            return ResponseSchema(
                code=ErrorCode.CONFIG_KEY_EXISTS, message="Config Key already exists"
            )
        if existing.name == form.name:
            return ResponseSchema(
                code=ErrorCode.CONFIG_NAME_EXISTS, message="Config Name already exists"
            )

    config.name = form.name
    config.key = form.key
    config.value = form.value
    config.type = form.type
    config.remark = form.remark
    config.update_by = current_user.username

    await db.commit()
    await db.refresh(config)
    return ResponseSchema(result=config)


@router.delete("/delete/{id}", response_model=ResponseSchema)
async def delete_config(
    id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    config = await db.get(SysConfig, id)
    if not config or config.delete_time is not None:
        return ResponseSchema(
            code=ErrorCode.CONFIG_NOT_FOUND, message="Config not found"
        )

    # Soft delete
    from datetime import datetime

    config.delete_time = datetime.now()
    config.delete_by = current_user.username

    await db.commit()
    return ResponseSchema(message="Success")
