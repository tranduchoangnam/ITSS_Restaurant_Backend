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


class Dish(SQLModel, BaseCreateUpdateModel, table=True):
    __tablename__: str = "dishes"
    __table_args__ = {
        "comment": "料理",
    }
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(
        sa_column=Column(String(255), nullable=True), default=None
    )
    address: Optional[str] = Field(sa_column=Column(Text), default=None)
    location: Optional[str] = Field(sa_column=Column(String(255)), default=None)
    price: Optional[int] = Field(sa_column=Column(Integer), default=None)
    info: Optional[str] = Field(sa_column=Column(Text), default=None)
    images: Optional[List[str]] = Field(
        sa_column=Column(ARRAY(String(2048))), default=None
    )
    categories: Optional[List[str]] = Field(
        sa_column=Column(ARRAY(String(255))), default=None
    )

    deleted_at: Optional[datetime] = Field(
        sa_column=Column(
            TIMESTAMP,
            nullable=True,
        ),
        default=None,
    )
