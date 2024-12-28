import enum
from datetime import datetime
from typing import Optional, List

from sqlalchemy import (
    TIMESTAMP,
    Column,
    Enum,
    String,
    Text,
    Boolean,
    Integer,
    ARRAY,
    Float,
)
from sqlmodel import Field, SQLModel

from backend.models.base import BaseCreateUpdateModel


class RoleCode(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class User(SQLModel, BaseCreateUpdateModel, table=True):
    __tablename__: str = "users"
    __table_args__ = {
        "comment": "ユーザー",
    }
    id: Optional[int] = Field(default=None, primary_key=True)
    role_code: Optional[RoleCode] = Field(sa_column=Column(Enum(RoleCode)))
    email: Optional[str] = Field(sa_column=Column(String(255)), default=None)
    password: Optional[str] = Field(
        sa_column=Column(String(2048), nullable=True), default=None
    )
    display_name: Optional[str] = Field(
        sa_column=Column(String(255), nullable=True), default=None
    )
    phone: Optional[str] = Field(sa_column=Column(String(20)), default=None)
    address: Optional[str] = Field(sa_column=Column(Text), default=None)
    location: Optional[str] = Field(sa_column=Column(String(255)), default=None)
    avatar_url: Optional[str] = Field(
        sa_column=Column(String(2048), nullable=True), default=None
    )
    # setting
    dark_mode: Optional[bool] = Field(sa_column=Column(Boolean), default=False)
    language: Optional[str] = Field(sa_column=Column(String(10)), default="ja")
    font_size: Optional[int] = Field(sa_column=Column(Integer), default=None)
    notification: Optional[bool] = Field(sa_column=Column(Boolean), default=True)

    # fav
    loved_flavor: Optional[List[str]] = Field(
        sa_column=Column(ARRAY(String(255))), default=None
    )
    hated_flavor: Optional[List[str]] = Field(
        sa_column=Column(ARRAY(String(255))), default=None
    )
    loved_dish:  Optional[List[str]] = Field(
        sa_column=Column(ARRAY(String(255))), default=None
    )
    vegetarian: Optional[bool] = Field(sa_column=Column(Boolean), default=False)
    loved_distinct: Optional[float] = Field(sa_column=Column(Float), default=None)
    loved_price: Optional[int] = Field(sa_column=Column(Integer), default=None)
    deleted_at: Optional[datetime] = Field(
        sa_column=Column(
            TIMESTAMP,
            nullable=True,
        ),
        default=None,
    )
