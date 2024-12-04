import re
from datetime import datetime
from typing import Annotated, Optional

from fastapi import Query
from pydantic import BaseModel, EmailStr, validator
from sqlmodel import Field

from backend.constants.account_status import AccountStatus
from backend.core.constant import ValidCode
from backend.core.error_code import ErrorCode, ErrorMessage
from backend.schemas.base import BaseResponse


class UserBase(BaseModel):
    id: Optional[int]
    role_code: Optional[str]
    email: Optional[str]
    display_name: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    avatar_url: Optional[str]


class BasicUserInformation(BaseModel):
    phone: Annotated[str, Field(description="電話番号")]
    address: Annotated[str, Field(description="市区町村番地・ビル名")]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "address": "Susukigahara, Kutsukimi, Nerima, Tokyo",
                    "phone": "09023456789",
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
    # tags: Optional[list[int]] = Field(default=None, description="tags list")

    # @validator("tags")
    # def check_tags_length(cls, v):
    #     if v is not None and len(v) > 10:
    #         raise ValueError("Tags can have at most 10 items")
    #     return v
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
    event_application_count: Annotated[int, Field(..., description="イベント参加回数")]
    followed_organization_count: Annotated[
        int, Field(..., description="フォロー中の主催者数")
    ]
    latest_event_attend_date: Annotated[
        datetime | None, Field(..., description="最新のイベント参加日")
    ]


class ListingUsersResponse(BaseResponse[ListingUsersItem]):
    pass


class FilteringUsersQueryParams(BaseModel):
    per_page: Annotated[int | None, Field(Query(default=10, le=50, ge=1))]
    page: Annotated[int | None, Field(Query(default=1, ge=1))]

    start_time: Annotated[
        datetime | None, Field(Query(default=None, description="登録期間で検索"))
    ]

    end_time: Annotated[
        datetime | None, Field(Query(default=None, description="登録期間で検索"))
    ]

    event_keyword: Annotated[
        str | None,
        Field(Query(default=None, description="イベント名・イベントNo.で検索")),
    ]

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
