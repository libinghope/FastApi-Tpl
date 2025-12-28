from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, func, or_
import bcrypt

from app.api import deps
from app.core import security
from app.models.sys.user import SysUser, SysUserRoleRef
from app.models.sys.dept import SysDept
from app.models.sys.role import SysRole
from app.schemas.sys.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserEditForm,
    ChangeStatusForm,
    ModifyPasswordForm,
    DeleteObjsForm,
    UserProfileForm,
    BindPhoneForm,
    BindEmailForm,
)
from app.schemas.response import ResponseSchema, PageSchema

router = APIRouter()

@router.get("/me", response_model=ResponseSchema[UserResponse])
async def get_user_me(
    user: SysUser = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_db),
):
    """
    Get current user info
    """
    # Fetch roles
    stmt = select(SysUserRoleRef.role_id).where(SysUserRoleRef.user_id == user.id)
    result = await db.execute(stmt)
    role_ids = result.scalars().all()
    
    # Create response
    user_resp = UserResponse.model_validate(user)
    user_resp.role_ids = list(role_ids)
    return ResponseSchema(data=user_resp)

@router.get("/list", response_model=ResponseSchema[PageSchema[UserResponse]])
async def list_users(
    keywords: Optional[str] = None,
    status: Optional[int] = None,
    date_range: Optional[List[str]] = Query(None),
    page_size: int = 10,
    page_number: int = 1,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    """
    Get user list
    """
    stmt = select(SysUser, SysDept.name.label("dept_name")).outerjoin(SysDept, SysUser.dept_id == SysDept.id)
    
    filters = []
    if keywords:
        filters.append(
            or_(
                SysUser.username.ilike(f"%{keywords}%"),
                SysUser.nickname.ilike(f"%{keywords}%"),
                SysUser.phone_number.ilike(f"%{keywords}%"),
            )
        )
    if status is not None:
        filters.append(SysUser.status == status)
    
    if date_range and len(date_range) == 2:
        try:
            start_date = datetime.strptime(date_range[0], "%Y-%m-%d")
            end_date = datetime.strptime(date_range[1], "%Y-%m-%d").replace(hour=23, minute=59, second=59)
            filters.append(SysUser.create_time.between(start_date, end_date))
        except ValueError:
            pass # Ignore invalid date format
            
    if filters:
        stmt = stmt.where(*filters)
        
    # Count
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = await db.scalar(count_stmt)
    
    # Paging
    # Paging
    stmt = stmt.offset((page_number - 1) * page_size).limit(page_size)
    result = await db.execute(stmt)
    
    # Process result to include dept info if needed, or just return users
    # We returned UserResponse in schemas, but here we might return a custom dict to match frontend
    # original returned: {"list": user_list, "total": total_count}
    # UserInfo had dept_info.
    
    users_with_dept = result.all() # list of (SysUser, dept_name) or just (SysUser,) if outer join selected specific cols
    
    # Collect user IDs
    user_ids = [row[0].id for row in users_with_dept if row[0]]
    
    # Fetch roles for all users in one query
    role_map = {}
    if user_ids:
        role_stmt = select(SysUserRoleRef).where(SysUserRoleRef.user_id.in_(user_ids))
        role_result = await db.execute(role_stmt)
        role_refs = role_result.scalars().all()
        
        for ref in role_refs:
            if ref.user_id not in role_map:
                role_map[ref.user_id] = []
            role_map[ref.user_id].append(ref.role_id)
            
    users = []
    for row in users_with_dept:
        u = row[0]
        # dept_name = row[1] # If we wanted to include dept name flattened
        
        u_dict = UserResponse.model_validate(u).model_dump()
        u_dict['role_ids'] = role_map.get(u.id, [])
        users.append(u_dict)
        
    return ResponseSchema(data=PageSchema(list=users, total=total))

@router.post("/add", response_model=ResponseSchema)
async def add_user(
    form: UserEditForm,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    # Check username
    stmt = select(SysUser).where(SysUser.username == form.username)
    if await db.scalar(stmt):
        raise HTTPException(status_code=400, detail="Username already exists")
        
    new_user = SysUser(
        username=form.username,
        nickname=form.nickname,
        gender=form.gender,
        email=form.email,
        phone_number=form.phone_number,
        is_active=form.is_active if form.is_active is not None else True,
        dept_id=form.dept_id,
        hashed_password=security.get_password_hash(form.password or "123456"), # Default password
        create_by=current_user.username
    )
    db.add(new_user)
    await db.flush() # get id
    
    if form.role_ids:
        for rid in form.role_ids:
            db.add(SysUserRoleRef(user_id=new_user.id, role_id=rid))
            
    await db.commit()
    return ResponseSchema(message="Success")

@router.put("/update", response_model=ResponseSchema)
async def update_user(
    form: UserEditForm,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    if not form.id:
        raise HTTPException(status_code=400, detail="User ID is required")
        
    user = await db.get(SysUser, form.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Update fields
    if form.nickname is not None: user.nickname = form.nickname
    if form.gender is not None: user.gender = form.gender
    if form.email is not None: user.email = form.email
    if form.phone_number is not None: user.phone_number = form.phone_number
    if form.dept_id is not None: user.dept_id = form.dept_id
    if form.is_active is not None: user.is_active = form.is_active
    
    # Update updates info
    user.update_by = current_user.username
    
    # Roles
    if form.role_ids is not None:
        # Delete old roles
        await db.execute(delete(SysUserRoleRef).where(SysUserRoleRef.user_id == user.id))
        # Add new
        for rid in form.role_ids:
            db.add(SysUserRoleRef(user_id=user.id, role_id=rid))
            
    await db.commit()
    return ResponseSchema(message="Success")

@router.delete("/delete", response_model=ResponseSchema)
async def delete_users(
    form: DeleteObjsForm,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    # Cannot delete self
    if current_user.id in form.uid_arr:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    
    # Delete relationships first or rely on cascade? 
    # Usually cascade is set in DB, but let's be safe or just delete user.
    # Assuming CASCADE DELETE is configured or logically handled.
    # We will manually delete roles refs just in case.
    await db.execute(delete(SysUserRoleRef).where(SysUserRoleRef.user_id.in_(form.uid_arr)))
    
    await db.execute(delete(SysUser).where(SysUser.id.in_(form.uid_arr)))
    await db.commit()
    return ResponseSchema(message="Success")

@router.post("/reset/password", response_model=ResponseSchema)
async def reset_password(
    form: ModifyPasswordForm,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    user = await db.get(SysUser, form.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if form.password != form.password2:
        raise HTTPException(status_code=400, detail="Passwords do not match")
        
    user.hashed_password = security.get_password_hash(form.password)
    user.update_by = current_user.username
    await db.commit()
    
    relogin = (user.id == current_user.id)
    return ResponseSchema(data={"relogin": relogin})
    
@router.post("/change/active", response_model=ResponseSchema)
async def change_active_status(
    form: ChangeStatusForm,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    if form.user_uid == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot change your own status")
        
    user = await db.get(SysUser, form.user_uid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user.is_active = form.status
    user.update_by = current_user.username
    await db.commit()
    return ResponseSchema(message="Success")

@router.get("/options", response_model=ResponseSchema)
async def get_user_options(
    keywords: Optional[str] = None,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    stmt = select(SysUser)
    if keywords:
        stmt = stmt.where(SysUser.username.ilike(f"%{keywords}%"))
        
    result = await db.execute(stmt)
    users = result.scalars().all()
    
    return ResponseSchema(data={"result": [{"label": u.username, "value": u.id} for u in users]})
