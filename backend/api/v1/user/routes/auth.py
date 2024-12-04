from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path
from sqlmodel import Session

import backend.api.v1.user.services.auth as auth_service
import backend.api.v1.user.services.users as user_service
from backend.api.v1.dependencies.authentication import get_user_if_logged_in
from backend.core.config import settings
from backend.core.error_code import ErrorCode
from backend.core.exception import BadRequestException, UnauthorizedException
from backend.core.response import authenticated_api_responses, public_api_responses
from backend.db.database import get_db
from backend.models.user import User
from backend.schemas.auth import (
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    GetMeResponse,
    ResetPasswordRequest,
    ResetPasswordResponse,
    TokenResponse,
    UserLoginRequest,
)
from backend.schemas.user import (
    UserBaseResponse,
    InputRegisterUserRequest,
)
router = APIRouter()


@router.post("/login")
async def login(
    request: UserLoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    user = auth_service.authenticate_user(db, **request.model_dump())
    if not user:
        raise UnauthorizedException(ErrorCode.ERR_UNAUTHORIZED)
   
    access_token_expires = datetime.now() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = auth_service.create_access_token(
        data={"sub": user.email, "role": user.role_code}, expire=access_token_expires
    )
    refresh_token, refresh_expire_at = auth_service.create_refresh_token(
        {"sub": user.email, "role": user.role_code}, remember_me=request.remember_me
    )
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expire_at=access_token_expires,
        refresh_token=refresh_token,
        refresh_expire_at=refresh_expire_at,
    )

@router.post("/register", response_model=UserBaseResponse)
async def register_with_token(
    request: InputRegisterUserRequest,
    db: Session = Depends(get_db),
):
    kwargs = request.model_dump()
    new_user = await auth_service.register(db, **kwargs)
    user_dict = new_user.model_dump()
    return UserBaseResponse(**user_dict)

@router.get("/me", response_model=GetMeResponse, responses=authenticated_api_responses)
async def me(
    current_user: Annotated[User, Depends(get_user_if_logged_in)],
    db: Session = Depends(get_db),
):
    return GetMeResponse(
        id=current_user.id,
        role_code=current_user.role_code,
        email=current_user.email,
        display_name=current_user.display_name,
        phone=current_user.phone,
        address=current_user.address,
        avatar_url=current_user.avatar_url,
    )


@router.get("/refresh-token")
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db),
) -> TokenResponse:
    payload = auth_service.verify_refresh_token(refresh_token)

    user = auth_service.get_user_by_email(db, payload["sub"], payload["role"])
    if not user:
        raise UnauthorizedException(ErrorCode.ERR_UNAUTHORIZED)

    access_token_expires = datetime.now() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = auth_service.create_access_token(
        data={"sub": user.email, "role": user.role_code}, expire=access_token_expires
    )

    new_refresh_token, refresh_expire_at = auth_service.create_refresh_token(
        {"sub": user.email, "role": user.role_code}, remember_me=True
    )
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expire_at=access_token_expires,
        refresh_token=new_refresh_token,
        refresh_expire_at=refresh_expire_at,
    )



@router.post(
    "/reset-password",
    response_model=ResetPasswordResponse,
    responses=public_api_responses,
)
async def reset_password(
    db: Annotated[Session, Depends(get_db)],
    request: Annotated[
        ResetPasswordRequest,
        Body(
            title="Reset Password",
            description="Provide new password and confirm password.",
        ),
    ],
):
    await auth_service.reset_password(db, request)
    return ResetPasswordResponse(status="success", message="パスワードの再設定が完了しました。")

