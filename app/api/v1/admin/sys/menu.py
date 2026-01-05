from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, desc, distinct
from app.api import deps
from app.globals.constants import ROOT_ROUTER_PARENT_ID
from app.globals.enum import MenuType
from app.models.sys.menu import SysMenu, SysRoleMenu
from app.models.sys.role import SysRole
from app.models.sys.user import SysUser, SysUserRoleRef
from app.schemas.sys.menu import MenuCreate, MenuUpdate, MenuResponse, MenuTree
from app.schemas.response import ResponseSchema
from app.core.codes import ErrorCode
from pydantic import BaseModel
from app.globals.constants import ROOT_ROUTER_PARENT_ID

router = APIRouter()


class DeleteMenuForm(BaseModel):
    uid: int


@router.get("/list", response_model=ResponseSchema)
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

    return ResponseSchema(message="Success", result=build_menu_tree(menus, 0))


@router.post("/add", response_model=ResponseSchema)
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
            return ResponseSchema(
                code=ErrorCode.PARENT_MENU_NOT_FOUND, message="Parent menu not found"
            )
        new_menu.tree_path = f"{parent.tree_path},{parent.id}"

    db.add(new_menu)
    await db.commit()
    await db.refresh(new_menu)
    return ResponseSchema(
        message="Success", result=MenuResponse.model_validate(new_menu).model_dump()
    )


@router.post("/update", response_model=ResponseSchema)
async def update_menu(
    form: MenuUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    menu = await db.get(SysMenu, form.id)
    if not menu:
        return ResponseSchema(code=ErrorCode.MENU_NOT_FOUND, message="Menu not found")

    # Check parent loop
    if menu.id == form.parent_id:
        return ResponseSchema(
            code=ErrorCode.INVALID_ARGUMENT, message="Cannot set parent to self"
        )

    # Update logic with tree path handling
    old_parent_id = menu.parent_id
    old_tree_path = menu.tree_path

    for key, value in form.model_dump().items():
        setattr(menu, key, value)

    if old_parent_id != form.parent_id:
        if form.parent_id == 0:
            new_tree_path = "0"
        else:
            parent = await db.get(SysMenu, form.parent_id)
            if not parent:
                return ResponseSchema(
                    code=ErrorCode.PARENT_MENU_NOT_FOUND,
                    message="Parent menu not found",
                )
            new_tree_path = f"{parent.tree_path},{parent.id}"

        menu.tree_path = new_tree_path

        # Update children tree paths
        # We need to match precise children constraints to avoid updating unrelated paths
        # Old tree path: "0,1" -> Children start with "0,1,"
        search_path = f"{old_tree_path},{menu.id}"

        descendants_stmt = select(SysMenu).where(
            SysMenu.tree_path.like(f"{search_path}%")
        )
        descendants_result = await db.execute(descendants_stmt)
        descendants = descendants_result.scalars().all()

        new_level_tree_path = f"{new_tree_path},{menu.id}"

        for child in descendants:
            # suffix includes the comma separator usually if we slice correctly
            # child.tree_path = "0,1,5" -> suffix (len("0,1")) -> ",5"
            suffix = child.tree_path[len(search_path) :]
            # new path = "0,2,5" (if moved to 2) -> "0,2" + ",5" -> wait.
            # search_path included menu.id.
            # "0,1,5" (menu is 5). Child is 6 ("0,1,5,6").
            # search_path "0,1,5". len=5.
            # child path "0,1,5,6". suffix ",6".
            # new_level_tree_path "0,2,5".
            # child new path "0,2,5,6".
            child.tree_path = f"{new_level_tree_path}{suffix}"

    await db.commit()
    return ResponseSchema(message="Success")


@router.post("/delete", response_model=ResponseSchema)
async def delete_menu(
    form: DeleteMenuForm,
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    # Check children
    stmt = select(SysMenu).where(SysMenu.parent_id == form.uid)
    if await db.scalar(stmt):
        return ResponseSchema(
            code=ErrorCode.OPERATION_FAILED, message="Cannot delete menu with children"
        )

    await db.execute(delete(SysMenu).where(SysMenu.id == form.uid))
    await db.execute(delete(SysRoleMenu).where(SysRoleMenu.menu_id == form.uid))

    await db.commit()
    return ResponseSchema(message="Success")


def build_menu_tree(menus: List[SysMenu], parent_id: int) -> List[dict]:
    tree = []
    for menu in menus:
        if menu.parent_id == parent_id and menu.type != MenuType.BUTTON:
            # Convert menu to dict using vars() and exclude private attributes
            menu_dict = {
                key: value
                for key, value in vars(menu).items()
                if not key.startswith("_")
            }
            # Find children
            children = build_menu_tree(menus, menu.id)
            if children:
                menu_dict["children"] = children
            tree.append(menu_dict)
    return tree


def build_route_tree(menus: List[SysMenu], parent_id: int) -> List[dict]:
    tree = []
    for menu in menus:
        if menu.parent_id == parent_id:
            route = {
                "name": menu.name,
                "path": menu.route_path,
                "component": menu.component,
                "type": menu.type,
                "meta": {
                    "title": menu.name,
                    "icon": menu.icon,
                    "hidden": not menu.visible,
                    "keepAlive": True if menu.keep_alive == 1 else False,
                    "alwaysShow": True if menu.always_show == 1 else False,
                },
            }
            if menu.type == MenuType.CATALOG:  # Catalog
                route["redirect"] = menu.redirect
            children = build_route_tree(menus, menu.id)
            if children:
                route["children"] = children

            tree.append(route)
    return tree


@router.get("/routes", response_model=ResponseSchema)
async def get_current_user_routes(
    db: AsyncSession = Depends(deps.get_db),
    current_user: SysUser = Depends(deps.get_current_user),
):
    """
    Get routes for current user
    """
    if current_user.is_superuser:
        stmt = (
            select(SysMenu)
            .where(SysMenu.type != MenuType.BUTTON)
            .order_by(SysMenu.sort)
        )
    else:
        # Check user roles
        # SysUserRoleRef: user_id, role_id
        # SysRoleMenu: role_id, menu_id
        # We need menus where id in (select menu_id from role_menu where role_id in (select role_id from user_role where user_id = current_user.id))

        # Subquery for role ids
        sub_roles_ids = select(SysUserRoleRef.role_id).where(
            SysUserRoleRef.user_id == current_user.id
        )

        # Subquery for menu ids
        sub_menus = select(SysRoleMenu.menu_id).where(
            SysRoleMenu.role_id.in_(sub_roles_ids)
        )

        stmt = (
            select(SysMenu)
            .where(SysMenu.id.in_(sub_menus), SysMenu.type != MenuType.BUTTON)
            .order_by(SysMenu.sort)
        )

    result = await db.execute(stmt)
    menus = result.scalars().all()

    return ResponseSchema(result=build_route_tree(menus, ROOT_ROUTER_PARENT_ID))


# @router.get("/options", response_model=ResponseSchema)
# async def menu_options(
#     db: AsyncSession = Depends(deps.get_db),
#     current_user: SysUser = Depends(deps.get_current_user),
# ):
#     stmt = select(SysMenu).order_by(SysMenu.sort)
#     result = await db.execute(stmt)
#     menus = result.scalars().all()
#     return ResponseSchema(
#         message="Success", result=[m.model_dump() for m in build_menu_tree(menus, 0)]
#     )
