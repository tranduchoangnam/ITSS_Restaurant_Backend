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
    ForeignKey
)
from sqlmodel import Field, SQLModel

from backend.models.base import BaseCreateUpdateModel


class Review(SQLModel, BaseCreateUpdateModel, table=True):
    __tablename__: str = "reviews"
    __table_args__ = {
        "comment": "レビュー",
    }
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    dish_id: Optional[int] = Field(sa_column=Column(Integer, ForeignKey("dishes.id", ondelete="CASCADE")))
    rating: Optional[int] = Field(sa_column=Column(Integer), default=0)
    comment: Optional[str] = Field(sa_column=Column(Text), default=None)

    #user_id and dish_id are foreign keys to the User and Dish tables respectively


