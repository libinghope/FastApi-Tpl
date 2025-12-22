from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends
from api.globals.enum import NoticePublishStatus, NoticeTargetType
from api.globals.error import ErrorCode, NoticeErrorCode
from app.api.deps import get_current_user
from app.models.sys.user import SysUser as User
from api.models.sys.sys_notice import SysUserNotice
from api.schemes.admin.notice import (
    NoticeForm,
    NoticeInfo,
)
from api.schemes.admin.user import UserInfo
from conf.config_web import Config
from app.api.deps import get_db as get_async_session
from api.models.sys.sys_notice import SysNotice
from api.globals.response import response
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemes.base import DeleteObjsForm
from api.services.admin.notice_service import NoticeService, get_notice_service
from api.services.admin.user_service import UserService, get_user_service
import traceback

config = Config()
router = APIRouter(prefix="/backend", tags=["notice"])


# 获取通知公告列表
@router.get("/notices/list")
async def notice_list(
    title: str | None = "",
    page_number: int = 1,
    page_size: int = 20,
    user: User = Depends(get_current_user),
    notice_service: NoticeService = Depends(get_notice_service),
    user_service: UserService = Depends(get_user_service),
):
    notice_list, total_count, err = await notice_service.notice_list(
        title, page_number, page_size
    )
    if err != NoticeErrorCode.SUCCESS:
        return response(code=err)
    # notice_info_list = [
    #     NoticeInfo.model_validate(notice).model_dump() for notice in notice_list
    # ]
    notice_info_list = []
    for notice in notice_list:
        notice_info = NoticeInfo.model_validate(notice).model_dump()
        if notice_info["target_type"] == NoticeTargetType.ALL:
            notice_info["target_user_ids"] = []
        else:
            notice_info["target_user_ids"] = (
                notice.target_user_ids_str.split(",")
                if notice.target_user_ids_str
                else []
            )
        if notice.publisher_uid:
            publisher = await user_service.get_user(notice.publisher_uid)
            notice_info["publisher"] = publisher.username
        notice_info_list.append(notice_info)

    return response(result={"list": notice_info_list, "total": total_count})


@router.post("/notices/update")
async def update_notice(
    noticeUpdateForm: NoticeForm,
    user: User = Depends(get_current_user),
    notice_service: NoticeService = Depends(get_notice_service),
):
    err = notice_service.check_notice_form(noticeUpdateForm)
    if err != NoticeErrorCode.SUCCESS:
        return response(code=err)

    err = await notice_service.update_notice(noticeUpdateForm, user.uid)
    if err != NoticeErrorCode.SUCCESS:
        return response(code=err)

    return response()


# 撤回通知公告
@router.post("/notices/revoke/{notice_uid}")
async def withdraw_notice(
    notice_uid: str,
    user: User = Depends(get_current_user),
    notice_service: NoticeService = Depends(get_notice_service),
):
    err = await notice_service.notice_withdraw(notice_uid, user.uid)
    if err != NoticeErrorCode.SUCCESS:
        return response(code=err)
    return response()


# 发布通知公告
@router.post("/notices/publish/{notice_uid}")
async def publish_notice(
    notice_uid: str,
    user: User = Depends(get_current_user),
    notice_service: NoticeService = Depends(get_notice_service),
):
    err = await notice_service.notice_publish(notice_uid, user.uid)
    if err != NoticeErrorCode.SUCCESS:
        return response(code=err)
    return response()


# 所有通知公告已读
@router.post("/notices/allRead")
async def all_notice_read(
    user: User = Depends(get_current_user),
    notice_service: NoticeService = Depends(get_notice_service),
):
    err = await notice_service.read_all_my_notices(user)
    if err != NoticeErrorCode.SUCCESS:
        return response(code=err)
    return response()


# 新增通知公告
@router.post("/notices/add")
async def add_notice(
    noticeAddForm: NoticeForm,
    user: User = Depends(get_current_user),
    notice_service: NoticeService = Depends(get_notice_service),
):
    err = await notice_service.add_notice(noticeAddForm, user.uid)
    if err != NoticeErrorCode.SUCCESS:
        return response(code=err)
    return response()


# 获取通知公告详情
@router.get("/notices/detail/{notice_uid}")
async def notice_detail(
    notice_uid: str,
    user: User = Depends(get_current_user),
    notice_service: NoticeService = Depends(get_notice_service),
):
    notice, err = await notice_service.read_notice(notice_uid, user)
    if err != NoticeErrorCode.SUCCESS:
        return response(code=err)
    notice_info = NoticeInfo.model_validate(notice).model_dump()

    return response(result=notice_info)


# 获取我的通知公告列表
@router.get("/notices/my-list")
async def my_list(
    page_number: int = 1,
    page_size: int = 20,
    user: User = Depends(get_current_user),
    notice_service: NoticeService = Depends(get_notice_service),
):
    notices, total_count, err = await notice_service.query_my_notice_list(
        page_number, page_size, user.uid
    )
    if err != NoticeErrorCode.SUCCESS:
        return response(code=err)
    notice_info_list = []
    for notice in notices:
        notice_info = NoticeInfo.model_validate(notice).model_dump()
        if notice_info["target_type"] == NoticeTargetType.ALL:
            notice_info["target_user_ids"] = []
        else:
            notice_info["target_user_ids"] = (
                notice.target_user_ids_str.split(",")
                if notice.target_user_ids_str
                else []
            )
        notice_info_list.append(notice_info)
    return response(result={"list": notice_info_list, "total": total_count})


# 删除通知公告
@router.post("/notices/delete")
async def delete_many_noticenotices(
    id_arr: DeleteObjsForm,
    user: User = Depends(get_current_user),
    notice_service: NoticeService = Depends(get_notice_service),
):
    err = await notice_service.delete_notices(id_arr.uid_arr, user.uid)
    if err != NoticeErrorCode.SUCCESS:
        return response(code=err)
    return response()
