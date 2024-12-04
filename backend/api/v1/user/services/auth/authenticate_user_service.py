from sqlmodel import Session

from backend.api.v1.user.services.auth.get_user_service import get_user_by_email
from backend.api.v1.user.services.auth.secure_password_service import (
    verify_password,
)
from backend.schemas.user import UserBaseResponse

def authenticate_user(db: Session, **kwargs):
    user = get_user_by_email(db, kwargs.get("email"), kwargs.get("role_code"))
    print("user", user)
    if not user:
        return False

    if not verify_password(kwargs.get("password"), user.password):
        return False
    return UserBaseResponse(**user.model_dump())
