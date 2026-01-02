from fastapi import APIRouter

# from app.api.v1.admin import items as admin_items
# from app.api.v1.client import items as client_items
from app.api.v1.admin.sys import auth as admin_auth
from app.api.v1.admin.sys import user as admin_user
from app.api.v1.admin.sys import config as admin_config
from app.api.v1.admin.sys import dept as admin_dept
from app.api.v1.admin.sys import dict as admin_dict
from app.api.v1.admin.sys import dict_item as admin_dict_item
from app.api.v1.admin.sys import menu as admin_menu
from app.api.v1.admin.sys import role as admin_role
from app.api.v1.admin.sys import log as admin_log
from app.api.v1.admin.sys import notice as admin_notice

api_router = APIRouter()
# api_router.include_router(admin_items.router, prefix="/admin/items", tags=["admin-items"])
# api_router.include_router(client_items.router, prefix="/client/items", tags=["client-items"])
api_router.include_router(admin_auth.router, prefix="/admin/auth", tags=["admin-auth"])
api_router.include_router(
    admin_user.router, prefix="/admin/sys/user", tags=["admin-user"]
)
api_router.include_router(
    admin_config.router, prefix="/admin/sys/config", tags=["admin-config"]
)
api_router.include_router(
    admin_dept.router, prefix="/admin/sys/dept", tags=["admin-dept"]
)
api_router.include_router(
    admin_dict.router, prefix="/admin/sys/dict", tags=["admin-dict"]
)
api_router.include_router(
    admin_dict_item.router, prefix="/admin/sys/dict", tags=["admin-dict-item"]
)
api_router.include_router(
    admin_menu.router, prefix="/admin/sys/menu", tags=["admin-menu"]
)
api_router.include_router(
    admin_role.router, prefix="/admin/sys/role", tags=["admin-role"]
)
api_router.include_router(admin_log.router, prefix="/admin/sys/log", tags=["admin-log"])
api_router.include_router(
    admin_notice.router, prefix="/admin/sys/notice", tags=["admin-notice"]
)
