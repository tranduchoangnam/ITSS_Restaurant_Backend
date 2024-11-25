from fastapi import APIRouter

from .user import router as user_router

admin_routers = APIRouter()
admin_routers.include_router(user_router, prefix="/users", tags=["admin"])
