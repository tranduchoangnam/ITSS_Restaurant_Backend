import re
from datetime import datetime
from typing import Annotated, Optional, List

from fastapi import Query
from pydantic import BaseModel, EmailStr, validator
from sqlmodel import Field

from backend.constants.account_status import AccountStatus
from backend.core.constant import ValidCode
from backend.core.error_code import ErrorCode, ErrorMessage
from backend.schemas.base import BaseResponse


class DishBase(BaseModel):
    id: Optional[int]
    name: Optional[str]
    address: Optional[str]
    price: Optional[int]
    info: Optional[str]
    images: Optional[List[str]]
    categories: Optional[List[str]]
    deleted_at: Optional[datetime]


class ListingDishesResponse(BaseResponse[DishBase]):
    pass


class FilteringDishesQueryParams(BaseModel):
    per_page: Annotated[int | None, Field(Query(default=10, le=50, ge=1))]
    page: Annotated[int | None, Field(Query(default=1, ge=1))]

    name_keyword: Annotated[
        str | None,
        Field(Query(default=None)),
    ]

class CreateDishRequest(BaseModel):
    name: Optional[str]
    address: Optional[str]
    price: Optional[int]
    info: Optional[str]
    images: Optional[List[str]]
    categories: Optional[List[str]]
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "すし",
                    "address": "東京都新宿区",
                    "price": 1000,
                    "info": "美味しい",
                    "images": ["https://example.com/image.jpg"],
                    "categories": ["和食", "寿司"]
                }
            ]
        }
    }