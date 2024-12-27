import re
from datetime import datetime
from typing import Annotated, Optional, List

from fastapi import Query
from pydantic import BaseModel, EmailStr, validator
from sqlmodel import Field

from backend.core.error_code import ErrorCode, ErrorMessage
from backend.schemas.base import BaseResponse


class DishBase(BaseModel):
    id: Optional[int]
    name: Optional[str]
    address: Optional[str]
    location: Optional[str]
    price: Optional[int]
    info: Optional[str]
    images: Optional[List[str]]
    categories: Optional[List[str]]
    deleted_at: Optional[datetime]

class GetDishDetailResponse(DishBase):
    distance: Optional[float]
    pass

class ListingDishesResponse(BaseResponse[GetDishDetailResponse]):
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
                    "name": "Cơm thố Bách Khoa",
                    "address": "111 K2 Ng. 48 P. Tạ Quang Bửu, Bách Khoa, Hoàn Kiếm, Hà Nội, Vietnam",
                    "price": 50000,
                    "info": "美味しい",
                    "images": ["https://static.vinwonders.com/production/com-tho-da-nang-4.jpg"],
                    "categories": ["和食", "寿司"]
                }
            ]
        }
    }

class UpdateDishRequest(CreateDishRequest):
    pass