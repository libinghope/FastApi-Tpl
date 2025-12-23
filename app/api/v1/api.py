
from fastapi import APIRouter
# from app.api.v1.admin import items as admin_items
# from app.api.v1.client import items as client_items
from app.api.v1.admin.sys import auth as admin_auth
from app.api.v1.admin.sys import user as admin_user

api_router = APIRouter()
# api_router.include_router(admin_items.router, prefix="/admin/items", tags=["admin-items"])
# api_router.include_router(client_items.router, prefix="/client/items", tags=["client-items"])
api_router.include_router(admin_auth.router,prefix="/admin/auth", tags=["admin-auth"])
api_router.include_router(admin_user.router, prefix="/admin/sys/user", tags=["admin-user"])
