from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, desc, func

from app.api import deps
from app.models.sys.role import SysRole
from app.models.sys.menu import SysRoleMenu, SysMenu
from app.models.sys.user import SysUser
# from app.models.sys.user import SysUser as User # Avoid alias confusion
from app.schemas.sys.role import (
    RoleCreate,
    RoleUpdate,
    RoleResponse,
    DeleteObjsForm
)
from app.schemas.response import ResponseSchema, PageSchema
from pydantic import BaseModel

router = APIRouter()

class RoleAssignPermsForm(BaseModel):
    menu_ids: List[int]

@router.get("/list", response_model=ResponseSchema[PageSchema[RoleResponse]])
async def role_list(
    page: int = 1,
    size: int = 20,
    name: str = None,
    status: int = None,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    stmt = select(SysRole).order_by(desc(SysRole.create_time))
    if name:
        stmt = stmt.where(SysRole.name.like(f"%{name}%"))
    if status is not None:
        stmt = stmt.where(SysRole.status == status)
    
    # Count query
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = await db.scalar(count_stmt) or 0
    
    # Pagination
    stmt = stmt.offset((page - 1) * size).limit(size)
    result = await db.execute(stmt)
    roles = result.scalars().all()
    
    return ResponseSchema(data=PageSchema(
        list=[RoleResponse.model_validate(r).model_dump() for r in roles],
        total=total
    ))

@router.get("/options", response_model=ResponseSchema)
async def role_options(
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    stmt = select(SysRole).where(SysRole.status == 1).order_by(SysRole.sort)
    result = await db.execute(stmt)
    roles = result.scalars().all()
    return ResponseSchema(data={"result": [RoleResponse.model_validate(r).model_dump() for r in roles]})

@router.post("/add", response_model=ResponseSchema)
async def add_role(
    form: RoleCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    stmt = select(SysRole).where(SysRole.code == form.code)
    if await db.scalar(stmt):
        raise HTTPException(status_code=400, detail="Role code already exists")
        
    new_role = SysRole(**form.model_dump())
    new_role.create_by = current_user.username
    db.add(new_role)
    await db.commit()
    await db.refresh(new_role)
    return ResponseSchema(message="Success", data={"result": {"role_id": new_role.id}})

@router.post("/update", response_model=ResponseSchema)
async def update_role(
    form: RoleUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    role = await db.get(SysRole, form.id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
        
    if role.code != form.code:
        stmt = select(SysRole).where(SysRole.code == form.code)
        if await db.scalar(stmt):
            raise HTTPException(status_code=400, detail="Role code already exists")
            
    for key, value in form.model_dump().items():
        setattr(role, key, value)
        
    role.update_by = current_user.username
    await db.commit()
    return ResponseSchema(message="Success")

@router.post("/delete", response_model=ResponseSchema)
async def delete_roles(
    form: DeleteObjsForm,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    # Check if roles are assigned to users?
    # Keeping it simple for now, usually we check user_role link table if exists
    
    await db.execute(delete(SysRole).where(SysRole.id.in_(form.ids)))
    # Also delete role-menu associations?
    await db.execute(delete(SysRoleMenu).where(SysRoleMenu.role_id.in_(form.ids)))
    
    await db.commit()
    return ResponseSchema(message="Success")

@router.get("/{role_id}/menu_ids", response_model=ResponseSchema)
async def get_role_menu_ids(
    role_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    stmt = select(SysRoleMenu.menu_id).where(SysRoleMenu.role_id == role_id)
    result = await db.execute(stmt)
    menu_ids = result.scalars().all()
    return ResponseSchema(data={"result": menu_ids})

@router.post("/{role_id}/assign_perms", response_model=ResponseSchema)
async def assign_perms(
    role_id: int,
    form: RoleAssignPermsForm,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    role = await db.get(SysRole, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
        
    # Delete existing
    await db.execute(delete(SysRoleMenu).where(SysRoleMenu.role_id == role_id))
    
    # Add new
    if form.menu_ids:
        # Validate menu ids? optional
        values = [{"role_id": role_id, "menu_id": mid} for mid in form.menu_ids]
        await db.execute(insert(SysRoleMenu), values)
        
    await db.commit()
    return ResponseSchema(message="Success")

@router.post("/{role_id}/update_status", response_model=ResponseSchema)
async def update_role_status(
    role_id: int,
    status: bool = Query(..., description="Status (true: Normal, false: Disabled)"),
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    role = await db.get(SysRole, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
        
    role.status = 1 if status else 0
    role.update_by = current_user.username
    await db.commit()
    return ResponseSchema(message="Success")
