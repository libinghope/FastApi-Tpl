from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.config import settings
from app.api.v1.api import api_router
from app.core.codes import ErrorCode

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


# 全局异常处理
# @app.exception_handler(Exception)
# async def global_exception_handler(request: Request, exc: Exception):
#     """全局异常处理器"""
#     # 处理Pydantic验证异常
#     if isinstance(exc, RequestValidationError):
#         return JSONResponse(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             content=ResponseSchema(
#                 code=ErrorCode.INVALID_ARGUMENT,
#                 message="请求参数验证失败",
#                 data=exc.errors(),
#             ).model_dump(),
#         )

#     # 处理其他异常
#     else:
#         return JSONResponse(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             content=ResponseSchema(
#                 code=ErrorCode.OPERATION_FAILED, message=str(exc), data=None
#             ).model_dump(),
#         )


app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Template"}
