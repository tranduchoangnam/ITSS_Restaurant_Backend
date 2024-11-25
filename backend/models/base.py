from datetime import datetime
from typing import Optional

from sqlalchemy import TIMESTAMP, Integer, func
from sqlmodel import Field


class BaseCreateUpdateModel:
    created_at: datetime = Field(
        default=None,
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={
            "server_default": func.now(),
        },
    )
    updated_at: datetime = Field(
        default=None,
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={
            "onupdate": func.now(),
        },
    )
    created_by: Optional[int] = Field(
        sa_type=Integer,
        sa_column_kwargs={
            "nullable": True,
        },
        default=None,
    )
    updated_by: Optional[int] = Field(
        sa_type=Integer,
        sa_column_kwargs={
            "nullable": True,
        },
        default=None,
    )
