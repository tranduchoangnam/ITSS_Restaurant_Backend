import re
from datetime import datetime
from typing import Annotated, Optional, List

from fastapi import Query
from pydantic import BaseModel, EmailStr, validator
from sqlmodel import Field

from backend.core.error_code import ErrorCode, ErrorMessage
from backend.schemas.base import BaseResponse


class UploadResponse(BaseModel):
    url: str

