from fastapi import HTTPException, status
from app.core.codes import ErrorCode


class APIException(HTTPException):
    """自定义API异常类"""
    def __init__(self,
                 code: ErrorCode = ErrorCode.INVALID_ARGUMENT,
                 message: str = None,
                 status_code: int = None):
        if not status_code:
            status_code = error_code_to_http_status(code)
        if not message:
            message = error_code_to_message(code)
        
        self.code = code
        self.message = message
        super().__init__(status_code=status_code, detail=message)


def error_code_to_http_status(code: ErrorCode) -> int:
    """业务错误码到HTTP状态码的映射"""
    status_map = {
        # 成功
        ErrorCode.SUCCESS: status.HTTP_200_OK,
        
        # 客户端错误 (4xx)
        ErrorCode.INVALID_ARGUMENT: status.HTTP_400_BAD_REQUEST,
        ErrorCode.NOT_FOUND: status.HTTP_404_NOT_FOUND,
        ErrorCode.PERMISSION_DENIED: status.HTTP_403_FORBIDDEN,
        ErrorCode.USER_ALREADY_EXISTS: status.HTTP_400_BAD_REQUEST,
        ErrorCode.ROLE_ALREADY_EXISTS: status.HTTP_400_BAD_REQUEST,
        ErrorCode.DEPT_ALREADY_EXISTS: status.HTTP_400_BAD_REQUEST,
        ErrorCode.DICT_ALREADY_EXISTS: status.HTTP_400_BAD_REQUEST,
        ErrorCode.CONFIG_KEY_EXISTS: status.HTTP_400_BAD_REQUEST,
        ErrorCode.CONFIG_NAME_EXISTS: status.HTTP_400_BAD_REQUEST,
        ErrorCode.USER_NOT_FOUND: status.HTTP_404_NOT_FOUND,
        ErrorCode.ROLE_NOT_FOUND: status.HTTP_404_NOT_FOUND,
        ErrorCode.DEPT_NOT_FOUND: status.HTTP_404_NOT_FOUND,
        ErrorCode.PARENT_DEPT_NOT_FOUND: status.HTTP_404_NOT_FOUND,
        ErrorCode.DICT_NOT_FOUND: status.HTTP_404_NOT_FOUND,
        ErrorCode.DICT_ITEM_NOT_FOUND: status.HTTP_404_NOT_FOUND,
        ErrorCode.CONFIG_NOT_FOUND: status.HTTP_404_NOT_FOUND,
        ErrorCode.NOTICE_NOT_FOUND: status.HTTP_404_NOT_FOUND,
        ErrorCode.MENU_NOT_FOUND: status.HTTP_404_NOT_FOUND,
        ErrorCode.PARENT_MENU_NOT_FOUND: status.HTTP_404_NOT_FOUND,
        ErrorCode.PASSWORD_MISMATCH: status.HTTP_400_BAD_REQUEST,
        ErrorCode.PARENT_DEPT_DISABLED: status.HTTP_400_BAD_REQUEST,
        
        # 服务器错误 (5xx)
        ErrorCode.OPERATION_FAILED: status.HTTP_500_INTERNAL_SERVER_ERROR,
    }
    
    return status_map.get(code, status.HTTP_500_INTERNAL_SERVER_ERROR)


def error_code_to_message(code: ErrorCode) -> str:
    """错误码到默认错误消息的映射"""
    message_map = {
        # 成功
        ErrorCode.SUCCESS: "请求成功",
        
        # 通用错误
        ErrorCode.INVALID_ARGUMENT: "无效的参数",
        ErrorCode.NOT_FOUND: "资源不存在",
        ErrorCode.PERMISSION_DENIED: "权限不足",
        ErrorCode.OPERATION_FAILED: "操作失败",
        
        # 用户相关
        ErrorCode.USER_ALREADY_EXISTS: "用户名已存在",
        ErrorCode.USER_NOT_FOUND: "用户不存在",
        ErrorCode.PASSWORD_MISMATCH: "密码不匹配",
        
        # 角色相关
        ErrorCode.ROLE_ALREADY_EXISTS: "角色已存在",
        ErrorCode.ROLE_NOT_FOUND: "角色不存在",
        
        # 部门相关
        ErrorCode.DEPT_ALREADY_EXISTS: "部门已存在",
        ErrorCode.DEPT_NOT_FOUND: "部门不存在",
        ErrorCode.PARENT_DEPT_NOT_FOUND: "父部门不存在",
        ErrorCode.PARENT_DEPT_DISABLED: "父部门已禁用",
        
        # 菜单相关
        ErrorCode.MENU_NOT_FOUND: "菜单不存在",
        ErrorCode.PARENT_MENU_NOT_FOUND: "父菜单不存在",
        
        # 字典相关
        ErrorCode.DICT_ALREADY_EXISTS: "字典已存在",
        ErrorCode.DICT_NOT_FOUND: "字典不存在",
        ErrorCode.DICT_ITEM_NOT_FOUND: "字典项不存在",
        
        # 配置相关
        ErrorCode.CONFIG_KEY_EXISTS: "配置键已存在",
        ErrorCode.CONFIG_NAME_EXISTS: "配置名已存在",
        ErrorCode.CONFIG_NOT_FOUND: "配置不存在",
        
        # 通知相关
        ErrorCode.NOTICE_NOT_FOUND: "通知不存在",
    }
    
    return message_map.get(code, "未知错误")
