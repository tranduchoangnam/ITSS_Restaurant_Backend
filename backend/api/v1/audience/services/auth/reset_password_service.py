import hashlib
from datetime import datetime

from sqlmodel import Session, select

from backend.api.v1.audience.services.auth.secure_password_service import (
    get_password_hash,
)
from backend.core.error_code import ErrorCode, ErrorMessage
from backend.core.exception import BadRequestException
from backend.models.user import User
from backend.schemas.auth import ResetPasswordRequest, ResetPasswordTokenResponse


async def reset_password(db: Session, request: ResetPasswordRequest, reset_token: str):
    """
    Verify user based on reset token and reset user password
    """
    try:
        user = get_user_by_reset_password_token(db, reset_token)

        # Update user
        user.reset_password_token = user.reset_password_token_expire_at = None
        user.password = get_password_hash(request.new_password)
        user.updated_by = user.id
        user.updated_at = datetime.now()

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    except Exception as e:
        db.rollback()
        raise e


def get_user_by_reset_password_token(db: Session, reset_token: str) -> User:
    """
    Verify user based on reset token and reset user password
    """
    # Get encrypted token based on the reset token sent in email
    hashed_token = hashlib.sha256(reset_token.encode("utf-8")).hexdigest()
    # Find user based on reset token.
    user = db.exec(
        select(User).where(
            User.reset_password_token == hashed_token,
            User.reset_password_token_expire_at > datetime.now(),
        )
    ).first()
    if user is None:
        raise BadRequestException(
            ErrorCode.ERR_INVALID_RESET_PASSWORD_TOKEN,
            ErrorMessage.ERR_INVALID_RESET_PASSWORD_TOKEN,
        )
    return user


def check_valid_reset_password_token(db: Session, reset_token: str):
    user = get_user_by_reset_password_token(db, reset_token)
    return ResetPasswordTokenResponse(
        token=reset_token, expire_at=user.reset_password_token_expire_at
    )
