from typing import List
from fastapi import APIRouter, Depends
from api.globals.error import ErrorCode, RoleErrorCode
from api.libs.decorations.permission import has_permission
from api.services.admin.role_service import get_role_service, RoleService
from api.services.admin.menu_service import get_menu_service, MenuService
from app.api.deps import get_current_user
from app.models.sys.user import SysUser as User
from api.schemes.admin.role import RoleForm, RoleInfo, RoleAssignPermsForm
from conf.config_web import Config
from api.models.sys.sys_role import SysRole
from api.globals.response import response
from api.schemes.base import DeleteObjsForm
import traceback

config = Config()

router = APIRouter(prefix="/backend", tags=["role"])


@router.get("/roles/list")
async def role_list(
    user: User = Depends(get_current_user),
    role_service: RoleService = Depends(get_role_service),
):
    try:
        roles, err_code = await role_service.get_role_list()
        if err_code != RoleErrorCode.SUCCESS:
            return response(code=err_code)

        roles_list = [RoleInfo.model_validate(role).model_dump() for role in roles]

        return response(result={"list": roles_list, "total": len(roles)})
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return response(code=ErrorCode.UNKNOWN_ERROR)


# role下拉列表选项
@router.get("/roles/options", tags=["role"])
async def role_options(
    user: User = Depends(get_current_user),
    role_service: RoleService = Depends(get_role_service),
):
    try:
        roles, err_code = await role_service.build_role_options()
        if err_code != RoleErrorCode.SUCCESS:
            return response(code=err_code)
        role_list = [RoleInfo.model_validate(role).model_dump() for role in roles]
        return response(result=role_list)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return response(code=ErrorCode.UNKNOWN_ERROR)


# 新增角色
@router.post("/roles/add", tags=["role"])
# @has_permission("sys:role:add")
async def add_role(
    roleAddForm: RoleForm,
    user: User = Depends(get_current_user),
    role_service: RoleService = Depends(get_role_service),
):
    role_id, err_code = await role_service.add_role(roleAddForm, user.uid)
    if err_code != RoleErrorCode.SUCCESS:
        return response(code=err_code)
    return response(result={"role_id": role_id})


# 获取角色表单数据
@router.get("/role/{role_id}/form")
@has_permission("sys:role:query")
async def get_role_form_data(
    role_id: int,
    user: User = Depends(get_current_user),
    role_service: RoleService = Depends(get_role_service),
):
    try:
        for id in ids:
            role = await SysRole.get(db, id)
            if role and not role.is_deleted:
                # 判断当前角色是否了使用当中
                if await check_role_in_use(id, db):
                    await db.rollback()
                    return response(
                        code=RoleErrorCode.ROLE_IN_USE,
                        result={"role": role},
                        error_with_param=True,
                    )

                role.delete(delete_by=user.uid)
            else:
                return response(
                    code=RoleErrorCode.ROLE_NOT_FOUND,
                    result={"role": None},
                    error_with_param=True,
                )

        await db.commit()
        return response()
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        await db.rollback()
        return response(code=ErrorCode.UNKNOWN_ERROR)


# 修改角色
@router.post("/roles/update")
async def role_update(
    roleUpdateForm: RoleForm,
    user: User = Depends(get_current_user),
    role_service: RoleService = Depends(get_role_service),
):
    try:
        err_code = await role_service.update_role(roleUpdateForm, user.uid)
        if err_code != RoleErrorCode.SUCCESS:
            return response(code=err_code)
        return response()
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return response(code=ErrorCode.UNKNOWN_ERROR)


# 删除角色
@router.post("/roles/delete")
async def role_delete(
    deleteForm: DeleteObjsForm,
    user: User = Depends(get_current_user),
    role_service: RoleService = Depends(get_role_service),
):
    try:
        err_code = await role_service.delete_roles(deleteForm.uid_arr, user.uid)
        if err_code != RoleErrorCode.SUCCESS:
            return response(code=err_code)
        return response()
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return response(code=ErrorCode.UNKNOWN_ERROR)


# 获取角色的菜单ID集合
@router.get("/roles/menuIds/{role_uid}")
async def get_menu_ids_by_role_id(
    role_uid: str, menu_service: MenuService = Depends(get_menu_service)
):
    result = await menu_service.list_menu_uids_by_role_id(role_uid)
    return response(result=result)


# 分配菜单(权限)给角色
@router.post("/roles/assign-perms/{role_uid}")
# @has_permission("sys:role:assgin-menu")
async def assign_menus_to_role(
    role_uid: str,
    uids_form: RoleAssignPermsForm,
    user: User = Depends(get_current_user),
    role_service: RoleService = Depends(get_role_service),
):
    err_code = await role_service.assign_menus_to_role(
        role_uid, uids_form.menu_uids, user.uid
    )
    if err_code != RoleErrorCode.SUCCESS:
        return response(code=err_code)
    return response()


# 修改角色状态
@router.post("/role/{role_id}/update_status")
async def role_update_status(
    role_id: int,
    status: bool,
    user: User = Depends(get_current_user),
    role_service: RoleService = Depends(get_role_service),
):
    role = await SysRole.get(db, role_id)
    if not role:
        return response(RoleErrorCode.ROLE_NOT_FOUND)

    role.is_active = status
    role.update_by = user.uid
    await db.commit()
    return response()
