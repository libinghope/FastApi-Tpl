from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, desc, distinct

from app.api import deps
from app.models.sys.menu import SysMenu, SysRoleMenu
from app.models.sys.user import SysUser
from app.schemas.sys.menu import (
    MenuCreate,
    MenuUpdate,
    MenuResponse,
    MenuTree
)
from pydantic import BaseModel

router = APIRouter()

class DeleteMenuForm(BaseModel):
    uid: int

def build_menu_tree(menus: List[SysMenu], parent_id: int) -> List[MenuTree]:
    tree = []
    for menu in menus:
        if menu.parent_id == parent_id:
            node = MenuTree.model_validate(menu)
            children = build_menu_tree(menus, menu.id)
            if children:
                node.children = children
            tree.append(node)
    return tree

@router.get("/list", response_model=Any)
async def menu_list(
    keywords: str = None,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    stmt = select(SysMenu).order_by(SysMenu.sort)
    if keywords:
        stmt = stmt.where(SysMenu.name.like(f"%{keywords}%"))
    
    result = await db.execute(stmt)
    menus = result.scalars().all()
    
    return {"result": [m.model_dump() for m in build_menu_tree(menus, 0)]}

@router.post("/add")
async def add_menu(
    form: MenuCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    new_menu = SysMenu(**form.model_dump())
    
    # Handle tree path logic similar to dept
    if new_menu.parent_id == 0:
        new_menu.tree_path = "0"
    else:
        parent = await db.get(SysMenu, new_menu.parent_id)
        if not parent:
             raise HTTPException(status_code=404, detail="Parent menu not found")
        new_menu.tree_path = f"{parent.tree_path},{parent.id}"
        
    db.add(new_menu)
    await db.commit()
    await db.refresh(new_menu)
    return {"code": 200, "message": "Success", "result": new_menu.model_dump()}

@router.post("/update")
async def update_menu(
    form: MenuUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    menu = await db.get(SysMenu, form.id)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    
    # Check parent loop
    if menu.id == form.parent_id:
        raise HTTPException(status_code=400, detail="Cannot set parent to self")

    # Update logic with tree path handling
    old_parent_id = menu.parent_id
    
    for key, value in form.model_dump().items():
        setattr(menu, key, value)
        
    if old_parent_id != form.parent_id:
        if form.parent_id == 0:
            new_tree_path = "0"
        else:
            parent = await db.get(SysMenu, form.parent_id)
            if not parent:
                raise HTTPException(status_code=404, detail="Parent menu not found")
            new_tree_path = f"{parent.tree_path},{parent.id}"
            
        old_tree_path = f"{menu.tree_path},{menu.id}"
        new_level_tree_path = f"{new_tree_path},{menu.id}"
        
        menu.tree_path = new_tree_path
        
        # Update children tree paths
        descendants_stmt = select(SysMenu).where(SysMenu.tree_path.like(f"{old_tree_path}%"))
        descendants_result = await db.execute(descendants_stmt)
        descendants = descendants_result.scalars().all()
        
        for child in descendants:
            suffix = child.tree_path[len(old_tree_path):]
            child.tree_path = f"{new_level_tree_path}{suffix}"
            
    await db.commit()
    return {"code": 200, "message": "Success"}

@router.post("/delete")
async def delete_menu(
    form: DeleteMenuForm,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    # Check children
    stmt = select(SysMenu).where(SysMenu.parent_id == form.uid)
    if await db.scalar(stmt):
        raise HTTPException(status_code=400, detail="Cannot delete menu with children")
        
    await db.execute(delete(SysMenu).where(SysMenu.id == form.uid))
    await db.execute(delete(SysRoleMenu).where(SysRoleMenu.menu_id == form.uid))
    
    await db.commit()
    return {"code": 200, "message": "Success"}

@router.get("/routes")
async def get_current_user_routes(
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    
    # Let's check `SysUser` content after this write, 
    # BUT I am writing the file now. 
    # I will put a placeholder for routes logic or a simple "all menus" if user is superuser etc.
    # Better: implementing `get_routes` properly requires knowing how users are linked to roles.
    # I will use a subquery approach assuming table names `sys_user_role`.
    
    # Actually, I'll read `app/models/sys/user.py` after this tool call to be sure, and then update `menu.py` if needed.
    # For now, I will implement `menu_options` and others.
    
    return {"result": []} # Placeholder to be updated

@router.get("/options")
async def menu_options(
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    stmt = select(SysMenu).order_by(SysMenu.sort)
    result = await db.execute(stmt)
    menus = result.scalars().all()
    return {"result": [m.model_dump() for m in build_menu_tree(menus, 0)]}
