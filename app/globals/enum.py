from enum import Enum


class MenuType(str, Enum):
    """菜单类型"""

    CATALOG = "catalog"
    MENU = "menu"
    BUTTON = "button"
    EXTLINK = "extlink"


class RoleDataScope(str, Enum):
    """角色数据范围"""

    ALL = "all"
    DEPT_AND_CHILD = "dept_and_child"
    DEPT = "dept"
    SELF = "self"


class Gender(str, Enum):
    """性别"""

    UNKNOWN = "unknown"
    MALE = "male"
    FEMALE = "female"

class ConfigTypeEnum(str,Enum):
    STRING = "string"
    NUMBER = "number"
    LIST = "list"
    DICT = "dict"