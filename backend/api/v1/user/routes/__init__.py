from fastapi import APIRouter

from .auth import router as auth_router
from .user import router as user_router
from .dish import router as dish_router
from .upload import router as upload_router
user_routers = APIRouter()

user_routers.include_router(auth_router, tags=["auth"])
user_routers.include_router(user_router, prefix="/users", tags=["user"])
user_routers.include_router(dish_router, prefix="/dishes", tags=["dish"])
user_routers.include_router(upload_router, prefix="/upload", tags=["upload"])