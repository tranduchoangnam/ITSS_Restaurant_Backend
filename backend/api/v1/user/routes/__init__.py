from fastapi import APIRouter

from .auth import router as auth_router
from .user import router as user_router

user_routers = APIRouter()

user_routers.include_router(auth_router, tags=["auth"])
user_routers.include_router(user_router, prefix="/users", tags=["user"])