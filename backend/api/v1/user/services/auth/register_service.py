from datetime import datetime

from sqlmodel import Session, select

import backend.api.v1.user.services.auth as auth_service
from backend.api.v1.user.services.auth.get_user_service import get_user_by_email
from backend.core.config import settings
from backend.core.error_code import ErrorCode
from backend.core.exception import BadRequestException
from backend.models.user import RoleCode, User


async def register(db: Session, **kwargs):
    user = get_user_by_email(db, kwargs.get("email"), RoleCode.USER)
    if user:
        raise BadRequestException(ErrorCode.ERR_USER_ALREADY_EXISTS)

    new_user = User(
        email=kwargs.get("email"),
        display_name=kwargs.get("display_name"),
        role_code=RoleCode.USER,
        password=auth_service.get_password_hash(kwargs.get("password")),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    new_user = commit_user(db, new_user)
    return new_user


def commit_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


