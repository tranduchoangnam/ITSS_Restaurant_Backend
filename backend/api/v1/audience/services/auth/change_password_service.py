from datetime import datetime

from sqlmodel import Session, select

from backend.api.v1.audience.services.auth.secure_password_service import (
    get_password_hash,
)
from backend.core.error_code import ErrorCode
from backend.core.exception import BadRequestException, UnauthorizedException
from backend.models.user import User
from backend.schemas.auth import ChangePasswordRequest


def change_password(db: Session, token: str, request: ChangePasswordRequest):
    user = db.exec(select(User).where(User.reset_password_token == token)).first()

    if not user:
        raise UnauthorizedException(ErrorCode.ERR_UNAUTHORIZED)

    if user.reset_password_token_expire_at < datetime.now():
        raise BadRequestException(ErrorCode.ERR_TOKEN_EXPIRED)

    password = get_password_hash(request.new_password)
    user.password = password
    user.reset_password_token = None
    user.reset_password_token_expire_at = None

    db.commit()
