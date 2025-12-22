from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from api.globals.error import ErrorCode
from app.api.deps import get_current_user
from app.models.sys.user import SysUser as User
from api.schemes.admin.dict import DictForm, DictInfo
from conf.config_web import Config
from app.api.deps import get_db as get_async_session
from api.models.sys.sys_dict import SysDict
from api.globals.response import response
from sqlalchemy.ext.asyncio import AsyncSession
from api.globals.enum import GenderMapping
from api.services.admin.dict_service import DictService, get_dict_service
from api.schemes.base import DeleteObjsForm

import traceback

config = Config()

router = APIRouter(prefix="/backend", tags=["dict"])


@router.get("/dicts/list")
async def dict_list(
    keywords: str | None = "",
    page_size: int = 10,
    page_number: int = 1,
    user: User = Depends(get_current_user),
    dict_service: DictService = Depends(get_dict_service),
):
    dict_list, total, error_code = await dict_service.query_dicts_list(keywords)
    if error_code != ErrorCode.SUCCESS:
        return response(code=error_code)
    dict_info_list = [DictInfo.model_validate(d).model_dump() for d in dict_list]
    return response(result={"list": dict_info_list, "total": total})


@router.post("/dicts/add")
async def add_dict(
    dictForm: DictForm,
    user: User = Depends(get_current_user),
    dict_service: DictService = Depends(get_dict_service),
):
    error_code = await dict_service.add_dict(dictForm, user.uid)
    if error_code != ErrorCode.SUCCESS:
        return response(code=error_code)
    return response()


# 获取字典表单数据
# @router.get("/dict/{dict_uid}/form")
# async def get_dict_form(dict_uid: int):
#     try:
#         dict_entity = await SysDict.get(db, dict_uid)
#         if not dict_entity:
#             return response(code=ErrorCode.DICT_NOT_FOUND)

#         dict_form = DictForm.model_validate(dict_entity)
#         return response(result=dict_form)
#     except Exception as e:
#         print(e)
#         print(traceback.format_exc())
#         return response(code=ErrorCode.UNKNOWN_ERROR)


@router.post("/dicts/update")
async def update_dict(
    dictForm: DictForm,
    user: User = Depends(get_current_user),
    dict_service: DictService = Depends(get_dict_service),
):
    error_code = await dict_service.update_dict(dictForm, user.uid)
    if error_code != ErrorCode.SUCCESS:
        return response(code=error_code)
    return response()


@router.post("/dicts/delete")
async def delete_dict(
    delete_form: DeleteObjsForm,
    user: User = Depends(get_current_user),
    dict_service: DictService = Depends(get_dict_service),
):
    error_code = await dict_service.delete_dicts(delete_form.uid_arr, user.uid)
    if error_code != ErrorCode.SUCCESS:
        return response(code=error_code)
    return response()
