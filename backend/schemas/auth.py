from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, StringConstraints, validator
from sqlmodel import Field

from backend.schemas.user import UserBaseResponse

class UserLoginRequest(BaseModel):
    email: str
    password: str
    role_code: str
    remember_me: bool
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "example@gmail.com",
                    "role_code": "USER",
                    "password": "12345678",
                    "remember_me": True,
                }
            ]
        }
    }
    


class TokenResponse(BaseModel):
    token_type: str
    access_token: str
    expire_at: datetime
    refresh_token: str
    refresh_expire_at: datetime
    
class GetMeResponse(UserBaseResponse):
    pass

class ChangePasswordRequest(BaseModel):
    new_password: str


class ForgotPasswordRequest(BaseModel):
    email: Annotated[EmailStr, Field(description="登録しているメールアドレス")]
    role_code: str


class ForgotPasswordResponse(BaseModel):
    email: EmailStr
    expire_at: datetime


class ResetPasswordRequest(BaseModel):
    email: Annotated[EmailStr, Field(description="登録しているメールアドレス")]
    old_password: Annotated[
        str, StringConstraints(min_length=8), Field(description="現在のパスワード")
    ]
    role_code: Annotated[str, Field(description="ユーザーのロール")]
    new_password:Annotated[
        str, StringConstraints(min_length=8), Field(description="新パスワード")
    ]

    confirm_password: Annotated[
        str, StringConstraints(min_length=8), Field(description="新パスワード（確認）")
    ]

    @validator("confirm_password")
    def validate_confirm_password(cls, v, values) -> str:
        if "new_password" in values and v != values["new_password"]:
            raise ValueError("Passwords do not match")
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "example@gmail.com",
                    "old_password": "12345678",
                    "role_code": "USER",
                    "new_password": "123456789",
                    "confirm_password": "123456789",
                }
            ]
        }
    }


class ResetPasswordResponse(BaseModel):
    status: str
    message: str

