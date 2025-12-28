from enum import Enum

class ErrorCode(str, Enum):
    # Success
    SUCCESS = 'SUCCESS' # Keep 200 as integer for success if needed, or use "SUCCESS" string? 
                  # ImplementationPlan said mixed. 
                  # But str, Enum means all values are strings. 
                  # Let's make it simple: Inherit str, but if we need int 200 we just don't use this Enum for success.
                  # Or strict with plan: "SUCCESS = 200" in a class inheriting (str, Enum) might error if 200 is not str.
                  # Let's use simple Enum and mixed types or just rely on 200 literal in ResponseSchema defaults.
                  # For now, let's define only Errors here as requested.
    
    # Common
    INVALID_ARGUMENT = "INVALID_ARGUMENT"
    NOT_FOUND = "NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    OPERATION_FAILED = "OPERATION_FAILED"
    
    # User
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    PASSWORD_MISMATCH = "PASSWORD_MISMATCH"
    
    # Role
    ROLE_ALREADY_EXISTS = "ROLE_ALREADY_EXISTS"
    ROLE_NOT_FOUND = "ROLE_NOT_FOUND"
    
    # Dept
    DEPT_ALREADY_EXISTS = "DEPT_ALREADY_EXISTS"
    DEPT_NOT_FOUND = "DEPT_NOT_FOUND"
    PARENT_DEPT_NOT_FOUND = "PARENT_DEPT_NOT_FOUND"
    PARENT_DEPT_DISABLED = "PARENT_DEPT_DISABLED"
    
    # Menu
    MENU_NOT_FOUND = "MENU_NOT_FOUND"
    PARENT_MENU_NOT_FOUND = "PARENT_MENU_NOT_FOUND"
    
    # Dict
    DICT_ALREADY_EXISTS = "DICT_ALREADY_EXISTS"
    DICT_NOT_FOUND = "DICT_NOT_FOUND"
    DICT_ITEM_NOT_FOUND = "DICT_ITEM_NOT_FOUND"
    
    # Config
    CONFIG_KEY_EXISTS = "CONFIG_KEY_EXISTS"
    CONFIG_NAME_EXISTS = "CONFIG_NAME_EXISTS"
    CONFIG_NOT_FOUND = "CONFIG_NOT_FOUND"
    
    # Notice
    NOTICE_NOT_FOUND = "NOTICE_NOT_FOUND"
