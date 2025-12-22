from typing import List
from fastapi import APIRouter, Depends
from api.globals.error import ErrorCode
from api.services.admin.dept_service import DeptService, get_dept_service
from app.api.deps import get_current_user
from app.models.sys.user import SysUser as User
from api.schemes.admin.dept import DeptForm, DeptInfo
from conf.config_web import Config
from app.api.deps import get_db as get_async_session
from api.models.sys.sys_dept import SysDept
from api.globals.response import response
from sqlalchemy.ext.asyncio import AsyncSession
from api.globals.error import DeptErrorCode
from api.globals.constants import ROOT_NODE_PARENT_UID
from api.schemes.base import DeleteObjsForm
import traceback

config = Config()
router = APIRouter(prefix="/backend", tags=["dept"])


@router.post("/dept/update")
async def update_dept(
    deptUpdateForm: DeptForm,
    user: User = Depends(get_current_user),
    dept_service: DeptService = Depends(get_dept_service),
):
    error_code = await dept_service.update_dept(deptUpdateForm, user.uid)
    if error_code != DeptErrorCode.SUCCESS:
        return response(code=error_code)
    return response()


@router.get("/dept/tree")
async def dept_tree(
    name: str | None = "",
    user: User = Depends(get_current_user),
    dept_service: DeptService = Depends(get_dept_service),
):
    try:
        dept_list, error_code = await dept_service.build_depts_list(keywords=name)
        if error_code != DeptErrorCode.SUCCESS:
            return response(code=error_code)
        dept_tree = build_dept_children(ROOT_NODE_PARENT_UID, dept_list)

        return response(result=[dept.model_dump() for dept in dept_tree])
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return response(code=ErrorCode.UNKNOWN_ERROR)


@router.post("/dept/add")
async def add_dept(
    deptAddForm: DeptForm,
    user: User = Depends(get_current_user),
    dept_service: DeptService = Depends(get_dept_service),
):
    error_code = await dept_service.add_dept(deptAddForm, user.uid)
    if error_code != DeptErrorCode.SUCCESS:
        return response(code=error_code)
    return response()


# 获取部门下拉列表
@router.get("/dept/options")
async def get_dept_options(
    name: str | None = "",
    user: User = Depends(get_current_user),
    dept_service: DeptService = Depends(get_dept_service),
):
    dept_list, error_code = await dept_service.build_depts_list(keywords=name)
    if error_code != DeptErrorCode.SUCCESS:
        return response(code=error_code)
    dept_tree = build_dept_children(ROOT_NODE_PARENT_UID, dept_list)
    return response(result=[dept.model_dump() for dept in dept_tree])


@router.post("/dept/delete")
async def delete_dept(
    ids_form: DeleteObjsForm,
    user: User = Depends(get_current_user),
    dept_service: DeptService = Depends(get_dept_service),
):
    error_code = await dept_service.delete_depts(ids_form.uid_arr, user.uid)
    if error_code != DeptErrorCode.SUCCESS:
        return response(code=error_code)
    return response()


def build_dept_children(parent_uid: str, dept_list: List[SysDept]) -> List[DeptInfo]:
    children = []
    for dept in dept_list:
        if dept.parent_uid == parent_uid:
            dept_vo = DeptInfo.model_validate(dept)
            dept_vo.children = build_dept_children(dept_vo.uid, dept_list)
            children.append(dept_vo)
    return children
