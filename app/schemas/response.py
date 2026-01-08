from typing import Generic, TypeVar, Optional, Any, Union
from pydantic import BaseModel
from app.core.codes import ErrorCode

T = TypeVar("T")


class ResponseSchema(BaseModel, Generic[T]):
    """API响应通用Schema

    统一所有API的响应格式，包含业务错误码、响应消息和响应数据。
    """

    code: str = ErrorCode.SUCCESS
    """业务错误码，200表示成功"""
    message: str = "Success"
    """响应消息，描述操作结果"""
    result: Optional[T] = None
    """响应数据，泛型类型，根据接口返回具体数据"""

    class Config:
        from_attributes = True


class PageSchema(BaseModel, Generic[T]):
    """分页响应Schema

    用于分页查询接口的响应数据格式，包含数据列表和总记录数。
    """

    list: list[T]
    """分页数据列表"""
    total: int
    """总记录数"""


def response(
    code: str = ErrorCode.SUCCESS, message: str = "Success", data: Optional[T] = None
) -> ResponseSchema[T]:
    """便捷响应创建函数

    Args:
        code: 业务错误码
        message: 响应消息
        data: 响应数据

    Returns:
        统一格式的响应对象
    """
    return ResponseSchema(code=code, message=message, result=data)
