from fastapi import APIRouter, Depends
from api.libs.authentication import get_current_user
from api.globals.error import ErrorCode
from api.libs.decorations.permission import has_permission
from api.schemes.admin.config import ConfigForm, ConfigInfo
from conf.config_web import Config
from api.models.sys.sys_config import SysConfig
from api.globals.error import BackupErrorCode
from api.services.admin.backup_service import BackupService, get_backup_service
from api.schemes.admin.backup import BackupForm
from typing import List
from api.globals.response import response
import traceback

router = APIRouter()


@router.get("/list")
# @has_permission("sys:backup:query")
async def backupList(
    keywords: str = "",
    user: SysConfig = Depends(get_current_user),
    backup_service: BackupService = Depends(get_backup_service),
):
    backup_list, total_count, error_code = await backup_service.query_backup_list(
        keywords
    )
    if error_code != BackupErrorCode.SUCCESS:
        return response(code=error_code)
    # 恢复原始代码，因为现在response函数会自动处理枚举类型序列化
    backup_list = [
        ConfigInfo.model_validate(backup).model_dump() for backup in backup_list
    ]
    return response(result={"list": backup_list, "total": total_count})


@router.post("/add")
# @has_permission("sys:backup:add")
async def add_backup(
    backup_form: BackupForm,
    backup_service: BackupService = Depends(get_backup_service),
):
    error_code = await backup_service.add_backup(backup_form)
    if error_code != BackupErrorCode.SUCCESS:
        return response(code=error_code)

    return response()


@router.delete("/delete/{id}")
@has_permission("sys:backup:delete")
async def delete_backup(
    id: int,
    user: SysConfig = Depends(get_current_user),
    backup_service: BackupService = Depends(get_backup_service),
):
    error_code = await backup_service.delete_backup(id, user.uid)   
    if error_code != BackupErrorCode.SUCCESS:
        return response(code=error_code)

    return response()


@router.get("/download/{id}")
@has_permission("sys:backup:download")
async def download_backup(
    id: int,
    user: SysConfig = Depends(get_current_user),
    backup_service: BackupService = Depends(get_backup_service),
):
    download_url, error_code = await backup_service.get_download_url(id, user.uid)
    if error_code != BackupErrorCode.SUCCESS:
        return response(code=error_code)

    return response(result={"download_url": download_url})
