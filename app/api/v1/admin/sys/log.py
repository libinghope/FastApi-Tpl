from datetime import datetime
from fastapi import APIRouter, Depends, Query
from api.globals.error import ErrorCode
from app.api.deps import get_current_user
from app.models.sys.user import SysUser as User
from api.schemes.admin.log import LogInfo
from conf.config_web import Config
from app.api.deps import get_db as get_async_session
from api.models.sys.sys_log import SysLog as AccessLog
from api.globals.response import response
from sqlalchemy.ext.asyncio import AsyncSession
from api.services.admin.log_service import LogService, get_log_service
from api.globals.error import LogErrorCode

import traceback

config = Config()
router = APIRouter(prefix="/backend", tags=["log"])


@router.get("/logs/visit-trend")
async def visit_trend(
    title: str | None = "",
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    if not user.is_superuser:
        return response(code=ErrorCode.FORBIDDEN)
    try:
        r = {
            "dates": [
                "2024-06-30",
                "2024-07-01",
                "2024-07-02",
                "2024-07-03",
                "2024-07-04",
                "2024-07-05",
                "2024-07-06",
                "2024-07-07",
            ],
            "pvList": [1751, 5168, 4882, 5301, 4721, 4885, 1901, 1003],
            "uvList": None,
            "ipList": [207, 566, 565, 631, 579, 496, 222, 152],
        }
        return response(result=r)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return response(code=ErrorCode.UNKNOWN_ERROR)


@router.get("/logs/visit-stats")
async def visit_stats(
    title: str | None = "",
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    data = {
        "todayUvCount": 374,
        "totalUvCount": 16542,
        "uvGrowthRate": 0.34,
        "todayPvCount": 3766,
        "totalPvCount": 271258,
        "pvGrowthRate": 0.51,
    }
    return response(result=data)


@router.get("/logs/list")
async def log_list(
    keywords: str | None = "",
    date_range: list[str] | None = Query(
        default=None, description="例如 ?date_range=2025-07-01&date_range=2025-08-15"
    ),
    page_number: int = 1,
    page_size: int = 20,
    user: User = Depends(get_current_user),
    log_service: LogService = Depends(get_log_service),
):
    start_time = None
    end_time = None
    if date_range and len(date_range) == 2:
        try:
            start_time = datetime.strptime(date_range[0].strip(), "%Y-%m-%d")
            end_time = datetime.strptime(date_range[1].strip(), "%Y-%m-%d")
            end_time = end_time.replace(hour=23, minute=59, second=59)
        except ValueError:
            return response(
                code=LogErrorCode.QUERY_PARAM_ERROR,
                message="日期格式不正确，应为YYYY-MM-DD",
            )
    log_objs, total_count, code = await log_service.get_log_page(
        keywords=keywords,
        start_time=start_time,
        end_time=end_time,
        page_size=page_size,
        page_number=page_number,
    )
    log_infos = [LogInfo.model_validate(log_obj).model_dump() for log_obj in log_objs]
    return response(result={"list": log_infos, "total": total_count})
