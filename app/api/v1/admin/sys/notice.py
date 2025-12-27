from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, desc, and_, or_

from app.api import deps
from app.models.sys.notice import SysNotice, SysUserNotice
from app.models.sys.user import SysUser
from app.schemas.sys.notice import (
    NoticeCreate,
    NoticeUpdate,
    NoticeResponse,
)
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class DeleteObjsForm(BaseModel):
    ids: List[int]

@router.get("/list", response_model=Any)
async def notice_list(
    title: str = None,
    page: int = 1,
    size: int = 20,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    stmt = select(SysNotice).order_by(desc(SysNotice.create_time))
    if title:
        stmt = stmt.where(SysNotice.title.like(f"%{title}%"))
        
    result = await db.execute(stmt)
    all_notices = result.scalars().all()
    total = len(all_notices)
    
    start = (page - 1) * size
    end = start + size
    notices = all_notices[start:end]
    
    # Enrich with publisher info? Original did. 
    # But usually frontend just needs simple list. 
    # Original did: fetch publisher name. 
    # We can join with SysUser if needed, but let's stick to simple return first.
    
    return {
        "list": [NoticeResponse.model_validate(n).model_dump() for n in notices],
        "total": total
    }

@router.post("/add")
async def add_notice(
    form: NoticeCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    new_notice = SysNotice(**form.model_dump())
    new_notice.publisher_id = current_user.id
    new_notice.create_by = current_user.username
    
    db.add(new_notice)
    await db.commit()
    await db.refresh(new_notice)
    return {"code": 200, "message": "Success"}

@router.post("/update")
async def update_notice(
    form: NoticeUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    notice = await db.get(SysNotice, form.id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
        
    for key, value in form.model_dump().items():
        setattr(notice, key, value)
        
    notice.update_by = current_user.username
    await db.commit()
    return {"code": 200, "message": "Success"}

@router.post("/delete")
async def delete_notices(
    form: DeleteObjsForm,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    await db.execute(delete(SysNotice).where(SysNotice.id.in_(form.ids)))
    # Delete user associations?
    await db.execute(delete(SysUserNotice).where(SysUserNotice.notice_id.in_(form.ids)))
    await db.commit()
    return {"code": 200, "message": "Success"}

@router.get("/detail/{notice_id}")
async def notice_detail(
    notice_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    notice = await db.get(SysNotice, notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
        
    # Mark as read for current user if not already?
    # Logic: check if SysUserNotice exists, if not create, if exists check is_read.
    # Original `read_notice` service logic did this.
    
    stmt = select(SysUserNotice).where(
        and_(SysUserNotice.notice_id == notice_id, SysUserNotice.user_id == current_user.id)
    )
    user_notice = await db.scalar(stmt)
    if not user_notice:
        user_notice = SysUserNotice(
            notice_id=notice_id, 
            user_id=current_user.id, 
            is_read=True,
            read_time=datetime.now()
        )
        db.add(user_notice)
        await db.commit()
    elif not user_notice.is_read:
        user_notice.is_read = True
        user_notice.read_time = datetime.now()
        await db.commit()
        
    return {"result": NoticeResponse.model_validate(notice).model_dump()}

@router.post("/publish/{notice_id}")
async def publish_notice(
    notice_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    notice = await db.get(SysNotice, notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
        
    notice.publish_status = 1 # Published
    notice.publish_time = datetime.now()
    notice.update_by = current_user.username
    await db.commit()
    return {"code": 200, "message": "Success"}

@router.post("/revoke/{notice_id}")
async def revoke_notice(
    notice_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    notice = await db.get(SysNotice, notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
        
    notice.publish_status = 0 # Draft/Revoked
    notice.revoke_time = datetime.now()
    notice.update_by = current_user.username
    await db.commit()
    return {"code": 200, "message": "Success"}

@router.get("/my-list")
async def my_notice_list(
    page: int = 1,
    size: int = 20,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    # Logic: Notices that target this user valid.
    # target_type: 0 all, 1 specific.
    # If specific, check target_user_ids_str contains user_id? 
    # Or rely on SysUserNotice entries? 
    # Usually we query SysNotice where (target_type=All OR (target_type=Specific AND user_id in target_ids))
    # AND status=Published.
    
    # Original `notice.py` used `query_my_notice_list`.
    # Let's simple implementation:
    # Select * from sys_notice where publish_status=1 
    # Filter by user?
    
    # Since checking string `target_user_ids_str` in SQL is messy (`FIND_IN_SET` or like `%,id,%`), 
    # and we have `SysUserNotice` ... wait, `SysUserNotice` usually tracks read status.
    
    # Let's assume `target_user_ids_str` approach for simplified RBAC matching.
    # Better to fetch all published notices and filter in python if simplified.
    
    stmt = select(SysNotice).where(SysNotice.publish_status == 1).order_by(desc(SysNotice.publish_time))
    result = await db.execute(stmt)
    all_notices = result.scalars().all()
    
    valid_notices = []
    for notice in all_notices:
        if notice.target_type == 0: # All
            valid_notices.append(notice)
        elif notice.target_user_ids_str:
            target_ids = notice.target_user_ids_str.split(',')
            if str(current_user.id) in target_ids:
                valid_notices.append(notice)
                
    total = len(valid_notices)
    start = (page - 1) * size
    end = start + size
    ret_notices = valid_notices[start:end]
    
    return {
        "list": [NoticeResponse.model_validate(n).model_dump() for n in ret_notices],
        "total": total
    }

@router.post("/allRead")
async def read_all_notices(
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    # Mark all valid notices as read for this user.
    # Find all published notices effective for this user.
    # For each, ensure SysUserNotice exists and is_read=True.
    
    # Reuse my_list logic properly?
    # Simple way: Select all published notices where target matches.
    # For each, update/insert SysUserNotice.
    
    # This might be heavy if many notices.
    # Let's do it simply.
    
    stmt = select(SysNotice).where(SysNotice.publish_status == 1)
    result = await db.execute(stmt)
    all_notices = result.scalars().all()
    
    for notice in all_notices:
        is_target = False
        if notice.target_type == 0:
            is_target = True
        elif notice.target_user_ids_str and str(current_user.id) in notice.target_user_ids_str.split(','):
             is_target = True
             
        if is_target:
             stmt = select(SysUserNotice).where(
                 and_(SysUserNotice.notice_id == notice.id, SysUserNotice.user_id == current_user.id)
             )
             un = await db.scalar(stmt)
             if not un:
                 un = SysUserNotice(
                     notice_id=notice.id, 
                     user_id=current_user.id, 
                     is_read=True, 
                     read_time=datetime.now()
                 )
                 db.add(un)
             elif not un.is_read:
                 un.is_read = True
                 un.read_time = datetime.now()
                 
    await db.commit()
    return {"code": 200, "message": "Success"}
