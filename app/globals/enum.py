from enum import Enum


class MenuType(str, Enum):
    """菜单类型"""

    CATALOG = "catalog"
    MENU = "menu"
    BUTTON = "button"
    EXTLINK = "extlink"
