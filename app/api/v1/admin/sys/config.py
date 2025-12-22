from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from sqlalchemy import select
from api.globals.error import ErrorCode
from api.libs.decorations.permission import has_permission
from api.schemes.admin.config import ConfigForm, ConfigInfo
from conf.config_web import Config
from app.api.deps import get_db as get_async_session
from api.models.sys.sys_config import SysConfig
from api.globals.error import ConfigErrorCode
from api.services.admin.config_service import ConfigService, get_config_service
from typing import List
from api.globals.response import response
from sqlalchemy.ext.asyncio import AsyncSession
import traceback

router = APIRouter()
config = Config()
router = APIRouter(prefix="/backend", tags=["config"])


@router.get("/config/list")
# @has_permission("sys:config:query")
async def configList(
    keywords: str = "",
    user: SysConfig = Depends(get_current_user),
    config_service: ConfigService = Depends(get_config_service),
):
    config_list, total_count, error_code = await config_service.query_confs_list(
        keywords
    )
    if error_code != ConfigErrorCode.SUCCESS:
        return response(code=error_code)
    # 恢复原始代码，因为现在response函数会自动处理枚举类型序列化
    config_list = [
        ConfigInfo.model_validate(config).model_dump() for config in config_list
    ]
    return response(result={"list": config_list, "total": total_count})


@router.post("/config/update", tags=["config"])
@has_permission("sys:config:update")
async def update_config(
    config_form: ConfigForm,
    user: SysConfig = Depends(get_current_user),
    config_service: ConfigService = Depends(get_config_service),
):
    error_code = await config_service.update_config(config_form, user.uid)
    if error_code != ErrorCode.SUCCESS:
        return response(code=error_code)

    return response()


@router.post("/config/add")
@has_permission("sys:config:add")
async def add_config(
    config_form: ConfigForm,
    user: SysConfig = Depends(get_current_user),
    config_service: ConfigService = Depends(get_config_service),
):
    error_code = await config_service.add_config(config_form, user.uid)
    if error_code != ErrorCode.SUCCESS:
        return response(code=error_code)

    return response()


@router.delete("/config/delete/{uid}")
@has_permission("sys:config:delete")
async def delete_config(
    uid: str,
    user: SysConfig = Depends(get_current_user),
    config_service: ConfigService = Depends(get_config_service),
):
    error_code = await config_service.delete_config(uid, user.uid)
    if error_code != ErrorCode.SUCCESS:
        return response(code=error_code)

    return response()


async def check_config_form(
    config_form: ConfigForm, db: AsyncSession, id: int = -1
) -> ErrorCode:
    # 检查配置键是否重复
    stmt = await db.execute(
        select(SysConfig).where(
            SysConfig.config_key == config_form.key,
            SysConfig.id != config_form.id if id != -1 else True,
            SysConfig.is_deleted == False,
        )
    )
    config = stmt.scalars().first()
    if config:
        return ErrorCode.CONFIG_KEY_DUPLICATE

    # 检查配置名称是否重复
    stmt = await db.execute(
        select(SysConfig).where(
            SysConfig.config_name == config_form.config_name,
            SysConfig.id != config_form.id if id != -1 else True,
            SysConfig.is_deleted == False,
        )
    )
    config = stmt.scalars().first()
    if config:
        return ErrorCode.CONFIG_NAME_DUPLICATE

    return ErrorCode.SUCCESS
