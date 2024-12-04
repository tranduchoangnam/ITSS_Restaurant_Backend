import hashlib
from datetime import datetime

from sqlmodel import Session, select

from backend.api.v1.user.services.auth.secure_password_service import (
    get_password_hash,
)
from backend.core.error_code import ErrorCode, ErrorMessage
from backend.core.exception import BadRequestException
from backend.models.user import User
from backend.schemas.auth import ResetPasswordRequest
from backend.api.v1.user.services.auth import authenticate_user


async def reset_password(db: Session, request: ResetPasswordRequest):

    try:
        user = authenticate_user(
            db,
            email=request.email,
            password=request.old_password,
            role_code=request.role_code,
        )
        print(request.email, request.old_password)
        if not user:
            raise BadRequestException(
                ErrorCode.ERR_UNAUTHORIZED,
            )

        user = db.exec(select(User).where(User.email == request.email)).first()

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
