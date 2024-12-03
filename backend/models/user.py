import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import TIMESTAMP, Column, Enum, String, Text
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
    new_email: Optional[str] = Field(sa_column=Column(String(255)), default=None)
    password: Optional[str] = Field(
        sa_column=Column(String(2048), nullable=True), default=None
    )
    display_name: Optional[str] = Field(
        sa_column=Column(String(255), nullable=True), default=None
    )
    phone: Optional[str] = Field(sa_column=Column(String(20)), default=None)
    address: Optional[str] = Field(sa_column=Column(Text), default=None)
    avatar_url: Optional[str] = Field(
        sa_column=Column(String(2048), nullable=True), default=None
    )
    reset_password_token: Optional[str] = Field(
        sa_column=Column(String(2048), nullable=True), default=None
    )
    reset_password_token_expire_at: Optional[str] = Field(
        sa_column=Column(TIMESTAMP, nullable=True), default=None
    )
    deleted_at: Optional[datetime] = Field(
        sa_column=Column(
            TIMESTAMP,
            nullable=True,
        ),
        default=None,
    )
