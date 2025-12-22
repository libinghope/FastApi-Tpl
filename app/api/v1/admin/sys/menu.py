from fastapi import APIRouter, Depends
from api.globals.enum import MenuType
from api.globals.error import ErrorCode, RouteErrorCode, RoleErrorCode
from app.api.deps import get_current_user
from api.models.sys.sys_menu import SysMenu
from api.schemes.admin.menu import UpdateMenuForm, MenuInfo, DeleteMenuForm
from conf.config_web import Config
from api.globals.error import MenuErrorCode
from typing import List
from app.models.sys.user import SysUser as User
from api.globals.response import response
from api.services.admin.menu_service import MenuService, get_menu_service
from api.services.admin.role_service import RoleService, get_role_service
from api.globals.constants import ROOT_NODE_PARENT_UID
import traceback
from sqlalchemy import or_, select

config = Config()

router = APIRouter(prefix="/backend", tags=["menu"])


@router.post("/menu/update")
async def update_menu(
    menu_form: UpdateMenuForm,
    user: User = Depends(get_current_user),
    menu_service: MenuService = Depends(get_menu_service),
):
    error_code = await menu_service.update_menu(menu_form, update_by=user.uid)
    if error_code != MenuErrorCode.SUCCESS:
        return response(code=error_code)
    return response()


@router.get("/menu/list")
async def menu_list(
    keywords: str | None = "",
    user: User = Depends(get_current_user),
    menu_service: MenuService = Depends(get_menu_service),
):
    menus_objs = await menu_service.list_menus(keywords=keywords)
    menu_tree = build_menu_tree(ROOT_NODE_PARENT_UID, menus_objs)
    menu_tree = [m.model_dump() for m in menu_tree]
    return response(result=menu_tree)


@router.post("/menu/add")
async def add_menu(
    menu_form: UpdateMenuForm,
    user: User = Depends(get_current_user),
    menu_service: MenuService = Depends(get_menu_service),
):
    menu, error_code = await menu_service.add_menu(menu_form, create_by=user.uid)
    if error_code != MenuErrorCode.SUCCESS:
        return response(code=error_code)
    return response(result=menu.model_dump())


# 修改菜单显示状态
# @router.post("/update/menu/show_status")
# async def update_menu_status(
#     menu_id: int,
#     status: bool,
#     user: User = Depends(get_current_user),
#     menu_service: MenuService = Depends(get_menu_service),
# ):
#     menu = await SysMenu.get(db, menu_id)
#     if not menu:
#         return response(code=RouteErrorCode.MENU_NOT_FOUND)

#     menu.is_active = status
#     menu.update_by = user.uid
#     await db.commit()
#     return response()


# 删除菜单
@router.post("/menu/delete")
async def delete_menu(
    delete_form: DeleteMenuForm,
    user: User = Depends(get_current_user),
    menu_service: MenuService = Depends(get_menu_service),
):
    error_code = await menu_service.delete_menu(delete_form.uid, delete_by=user.uid)
    if error_code != MenuErrorCode.SUCCESS:
        return response(code=error_code)
    return response()


# 菜单路由列表
@router.get("/menu/routes")
async def get_current_user_routes(
    user: User = Depends(get_current_user),
    role_service: RoleService = Depends(get_role_service),
):
    roles, err_code = await role_service.get_roles_ids_by_user_uid(user.uid)
    if err_code != RoleErrorCode.SUCCESS:
        return response(code=err_code)

    routes, err_code = await role_service.list_routes_of_roles(roles)
    if err_code != RoleErrorCode.SUCCESS:
        return response(code=err_code)
    return response(result=routes)


@router.get("/menu/options")
async def menu_options(
    only_parent: bool = False,
    user: User = Depends(get_current_user),
    menu_service: MenuService = Depends(get_menu_service),
):
    """
    查询菜单选项
    """
    result = await menu_service.list_menus()
    menu_tree = build_menu_tree(ROOT_NODE_PARENT_UID, result)
    re = [m.model_dump() for m in menu_tree]
    return response(result=re)


def build_menu_tree(parent_uid: str, menu_list: List[SysMenu]) -> List[MenuInfo]:
    menu_tree = []
    for menu in menu_list:
        if menu.parent_uid == parent_uid:
            menu_vo = MenuInfo(
                uid=menu.uid,
                parent_uid=menu.parent_uid,
                tree_path=menu.tree_path,
                name=menu.name,
                type=menu.type,
                route_name=menu.route_name,
                route_path=menu.route_path,
                component=menu.component,
                perm=menu.perm,
                always_show=menu.always_show,
                keep_alive=menu.keep_alive,
                visible=menu.visible,
                sort=menu.sort,
                icon=menu.icon,
                redirect=menu.redirect,
                params=menu.params,
                children=build_menu_tree(menu.uid, menu_list),
            )
            menu_tree.append(menu_vo)
    return menu_tree
