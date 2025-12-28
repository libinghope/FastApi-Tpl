from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, Query
from app.api.deps import get_current_user
from app.models.sys.user import SysUser as User
from app.api.deps import get_db as get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.response import ResponseSchema, response
from app.core.codes import ErrorCode

import traceback

router = APIRouter(prefix="/backend", tags=["log"])


@router.get("/logs/visit-trend", response_model=ResponseSchema[dict])
async def visit_trend(
    title: str | None = "",
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    if not user.is_superuser:
        return response(code=ErrorCode.FORBIDDEN, message="Permission denied")
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
        return response(data=r)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return response(code=ErrorCode.UNKNOWN_ERROR, message="Unknown error")


@router.get("/logs/visit-stats", response_model=ResponseSchema[dict])
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
    return response(data=data)


@router.get("/logs/list", response_model=ResponseSchema[dict])
async def log_list(
    keywords: str | None = "",
    date_range: list[str] | None = Query(
        default=None, description="例如 ?date_range=2025-07-01&date_range=2025-08-15"
    ),
    page_number: int = 1,
    page_size: int = 20,
    user: User = Depends(get_current_user),
):
    # 简化实现，返回空列表
    return response(data={"list": [], "total": 0})
