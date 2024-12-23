import re
from datetime import datetime
from typing import Annotated, Optional

from fastapi import Query
from pydantic import BaseModel, EmailStr, validator
from sqlmodel import Field

from backend.core.constant import AccountStatus
from backend.core.error_code import ErrorCode, ErrorMessage
from backend.schemas.base import BaseResponse


class UserBase(BaseModel):
    id: Optional[int]
    role_code: Optional[str]
    email: Optional[str]
    display_name: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    location: Optional[str]
    avatar_url: Optional[str]
    dark_mode: Optional[bool]
    language: Optional[str]
    font_size: Optional[int]
    notification: Optional[bool]
    loved_flavor: Optional[list[str]]
    hated_flavor: Optional[list[str]]
    vegetarian: Optional[bool]
    loved_distinct: Optional[float]
    loved_price: Optional[int]


class BasicUserInformation(BaseModel):
    display_name: Annotated[
        Optional[str],
        Field(default=None, description="プロフィール表示名", max_length=255),
    ]
    phone: Annotated[str, Field(description="電話番号")]
    address: Annotated[str, Field(description="市区町村番地・ビル名")]
    avatar_url: Annotated[
        Optional[str],
        Field(default=None, description="プロフィール表示画像", max_length=2048),
    ]
    dark_mode: Annotated[bool, Field(default=False, description="ダークモード")]
    language: Annotated[str, Field(default="ja", description="言語")]
    font_size: Annotated[
        Optional[int],
        Field(default=None, description="フォントサイズ", ge=1),
    ]
    notification: Annotated[bool, Field(default=True, description="通知設定")]
    loved_flavor: Annotated[
        Optional[list[str]],
        Field(default=None, description="好きな味"),
    ]
    hated_flavor: Annotated[
        Optional[list[str]],
        Field(default=None, description="嫌いな味"),
    ]
    vegetarian: Annotated[bool, Field(default=False, description="ベジタリアン")]
    loved_distinct: Annotated[
        Optional[float],
        Field(default=None, description="好きな辛さ", ge=0),
    ]
    loved_price: Annotated[
        Optional[int],
        Field(default=None, description="好きな価格", ge=0),
    ]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "display_name": "example",
                    "address": "1 Đ. Đại Cồ Việt, Bách Khoa, Hai Bà Trưng, Hà Nội, Vietnam",
                    "phone": "09023456789",
                    "avatar_url": "https://example.com/avatar.jpg",
                    "dark_mode": False,
                    "language": "ja",
                    "font_size": 16,
                    "notification": True,
                    "loved_flavor": ["spicy", "sour"],
                    "hated_flavor": ["sweet"],
                    "vegetarian": False,
                    "loved_distinct": 3.5,
                    "loved_price": 1000,
                }
            ]
        }
    }


class InputRegisterUserRequest(BaseModel):
    email: EmailStr
    password: str

    @validator("password")
    def password_validator(cls, v):
        return password_validator(v)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "example@gmail.com",
                    "password": "12345678",
                }
            ]
        }
    }


class UpdateUserRequest(BasicUserInformation):
    pass


class UserBaseResponse(UserBase):
    pass


class UpdateUserPublicInformationRequest(BaseModel):
    display_name: Annotated[
        Optional[str],
        Field(default=None, description="プロフィール表示名", max_length=255),
    ]
    avatar_url: Annotated[
        Optional[str],
        Field(default=None, description="プロフィール表示画像", max_length=2048),
    ]

    @validator("avatar_url")
    def avatar_url_validator(cls, v):
        if not v.startswith("http"):
            raise ValueError(ErrorCode.ERR_INVALID_URL, ErrorMessage.ERR_INVALID_URL)
        return v


class ListingUsersItem(BaseModel):
    id: Annotated[int | None, Field(...)]
    created_at: Annotated[datetime, Field(..., description="登録日時")]
    name: Annotated[str, Field(..., description="利用者名")]

class ListingUsersResponse(BaseResponse[ListingUsersItem]):
    pass


class FilteringUsersQueryParams(BaseModel):
    per_page: Annotated[int | None, Field(Query(default=10, le=50, ge=1))]
    page: Annotated[int | None, Field(Query(default=1, ge=1))]

    name_keyword: Annotated[
        str | None,
        Field(Query(default=None, description="利用者ID・利用者名で検索")),
    ]

    status: Annotated[Optional[AccountStatus], Field(Query(default=None))]


def phone_validator(v):
    if not re.match("^[0-9]*$", v) or len(v) != 11:
        raise ValueError(ErrorCode.ERR_INVALID_PHONE, ErrorMessage.ERR_INVALID_PHONE)
    return v


def password_validator(v):
    if len(v) < 8:
        raise ValueError(
            ErrorCode.ERR_INVALID_PASSWORD, ErrorMessage.ERR_INVALID_PASSWORD
        )
    pattern = r"^[!-~]+$"
    if not re.match(pattern, v):
        raise ValueError(
            ErrorCode.ERR_INVALID_PASSWORD, ErrorMessage.ERR_INVALID_PASSWORD_WIDTH
        )
    return v
