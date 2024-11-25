from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import DirectoryPath, validator
from pydantic_settings import BaseSettings
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    DB_CONNECTION: Optional[str]
    DB_HOST: Optional[str]
    DB_PORT: Optional[str]
    DB_DATABASE: Optional[str]
    DB_USERNAME: Optional[str]
    DB_PASSWORD: Optional[str]
    ALGORITHM: Optional[str]
    SECRET_KEY: Optional[str]
    ACCESS_TOKEN_EXPIRE_MINUTES: Optional[int]
    REFRESH_TOKEN_EXPIRE_MINUTES: Optional[int]
    REFRESH_TOKEN_REMEMBERED_EXPIRE_MINUTES: Optional[int]

    EMAIL_CONFIRMATION_TOKEN_LENGTH: Optional[int]
    EMAIL_CONFIRMATION_TOKEN_EXPIRE_MINUTES: Optional[int]
    RESET_PASSWORD_TOKEN_LENGTH: Optional[int]
    RESET_PASSWORD_TOKEN_EXPIRE_MINUTES: Optional[int]
    FRONTEND_URL: Optional[str]
    EMAIL_ADMIN: Optional[str]
    SQLALCHEMY_DATABASE_URL: str = ""
    BUCKET_NAME: Optional[str]
    MEDIA_PATH: Optional[str]
    MEDIA_PATH_TMP_PREFIX: str = "tmp/"
    PUBLIC_CDN_URL: Optional[str]

    EMAIL_SENDER: Optional[str]
    ORG_BCC_MAIL: Optional[str]
    SENDER_NAME: Optional[str]

    @validator("SQLALCHEMY_DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str) and v:
            return v
        if not (connection := values.get("DB_CONNECTION")):
            raise ValueError(
                "must specify at least DB_CONNECTION or SQLALCHEMY_DATABASE_URL",
            )
        username = values.get("DB_USERNAME")
        password = values.get("DB_PASSWORD")
        host = values.get("DB_HOST")
        port = values.get("DB_PORT")
        database = values.get("DB_DATABASE")
        return URL(
            connection, username, password, host, port, database, []
        ).render_as_string(False)

    class Config:
        case_sensitive = True
        env_file = "backend/.env"
        env_file_encoding = "utf-8"


settings = Settings()
