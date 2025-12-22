from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from api.globals.error import ErrorCode, DictErrorCode
from app.api.deps import get_current_user
from app.models.sys.user import SysUser as User
from api.schemes.admin.dict_item import DictItemForm, DictItemInfo
from conf.config_web import Config
from app.api.deps import get_db as get_async_session
from api.globals.response import response
from sqlalchemy.ext.asyncio import AsyncSession
from api.services.admin.dict_item_service import (
    DictItemService,
    get_dict_item_service,
)
from api.schemes.base import DeleteObjsForm
import traceback

config = Config()
router = APIRouter(prefix="/backend", tags=["dict-item"])


# 根据字典code获取所有字典项
@router.get("/dict/items/{dict_code}/list")
async def get_dict_items(
    dict_code: str, dict_item_service: DictItemService = Depends(get_dict_item_service)
):

    dict_items, error_code = await dict_item_service.get_dict_items_by_code(dict_code)
    if error_code != ErrorCode.SUCCESS:
        return response(code=error_code)
    dict_items_list = [DictItemInfo.model_validate(d).model_dump() for d in dict_items]
    return response(result=dict_items_list)


@router.post("/dict/items/add")
async def add_dict(
    dictForm: DictItemForm,
    user: User = Depends(get_current_user),
    dict_item_service: DictItemService = Depends(get_dict_item_service),
):
    error_code = await dict_item_service.add_dict_item(dictForm, create_by=user.uid)
    if error_code != ErrorCode.SUCCESS:
        return response(code=error_code)
    return response()


@router.post("/dict/items/update")
async def update_dict(
    dictForm: DictItemForm,
    user: User = Depends(get_current_user),
    dict_item_service: DictItemService = Depends(get_dict_item_service),
):
    error_code = await dict_item_service.update_dict_item(dictForm, update_by=user.uid)
    if error_code != ErrorCode.SUCCESS:
        return response(code=error_code)
    return response()


@router.post("/dict/items/delete")
async def delete_dict(
    delete_form: DeleteObjsForm,
    user: User = Depends(get_current_user),
    dict_item_service: DictItemService = Depends(get_dict_item_service),
):
    error_code = await dict_item_service.delete_dict_items(
        delete_form.uid_arr, delete_by=user.uid
    )
    if error_code != ErrorCode.SUCCESS:
        return response(code=error_code)
    return response()
