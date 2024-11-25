from sqlmodel import Session

import backend.api.v1.audience.services.auth as auth_service
from backend.core.error_code import ErrorCode, ErrorMessage
from backend.core.exception import BadRequestException
from backend.schemas.auth import ForgotPasswordRequest, ForgotPasswordResponse
from backend.utils import add_commit_refresh_object, create_url


async def forgot_password(
    db: Session, request: ForgotPasswordRequest
) -> ForgotPasswordResponse:
    """
    Create encrypted reset password token, send email for user
    """
    try:
        # Get user basded on POSTed email
        user = auth_service.get_user_by_email(db, request.email, request.role_code)

        # Verify user if exist
        if user is None:
            raise BadRequestException(
                ErrorCode.ERR_USER_NOT_FOUND, ErrorMessage.ERR_USER_NOT_FOUND
            )

        if user.email_verify_at is None:
            raise BadRequestException(
                ErrorCode.ERR_USER_NOT_VERIFIED,
                ErrorMessage.ERR_USER_NOT_VERIFIED,
            )

        # Create new email verify token
        (
            reset_token,
            encrypted_token,
            expire_at,
        ) = auth_service.create_reset_password_token()

        # Update user reset password token and expire_at
        user.reset_password_token = encrypted_token
        user.reset_password_token_expire_at = str(expire_at)
        add_commit_refresh_object(db, user)

        # TODO

        return ForgotPasswordResponse(
            email=user.email,
            expire_at=user.reset_password_token_expire_at,
        )
    except Exception as e:
        db.rollback()
        raise e
