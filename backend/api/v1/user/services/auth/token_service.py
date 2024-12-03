import hashlib
import secrets
import string
from datetime import datetime, timedelta, timezone
from typing import Tuple

from jose import jwt

from backend.core.config import settings
from backend.core.error_code import ErrorCode
from backend.core.exception import UnauthorizedException


# 指定した長さのトークンを作成
def create_token(token_length: int):
    # 使用する文字セット: 英字と数字の組み合わせ
    characters = string.ascii_letters + string.digits

    # ランダムトークンの生成
    token = "".join(secrets.choice(characters) for _ in range(token_length))

    return token


# Eメールアドレス確認トークンを作成
def create_email_confirmation_token():
    expire = datetime.now() + timedelta(
        minutes=settings.EMAIL_CONFIRMATION_TOKEN_EXPIRE_MINUTES
    )
    return create_token(settings.EMAIL_CONFIRMATION_TOKEN_LENGTH), expire


def create_refresh_token(data: dict, remember_me: bool) -> Tuple[str, datetime]:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(
        minutes=(
            settings.REFRESH_TOKEN_REMEMBERED_EXPIRE_MINUTES
            if remember_me
            else settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
    )

    to_encode.update({"exp": expire.astimezone(timezone.utc)})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt, expire


def create_access_token(data: dict, expire: datetime):
    to_encode = data.copy()
    to_encode.update({"exp": expire.astimezone(timezone.utc)})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_refresh_token(token: str):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    if payload["exp"] < datetime.now().timestamp():
        raise UnauthorizedException(ErrorCode.ERR_TOKEN_EXPIRED)
    if not payload["sub"]:
        raise UnauthorizedException(ErrorCode.ERR_UNAUTHORIZED)
    return payload


def create_reset_password_token():
    expire_at = datetime.now() + timedelta(
        minutes=settings.RESET_PASSWORD_TOKEN_EXPIRE_MINUTES
    )

    # Unencrypted reset token
    reset_token = create_token(settings.RESET_PASSWORD_TOKEN_LENGTH)

    # Encrypt reset token
    encrypted_token = hashlib.sha256(reset_token.encode("utf-8")).hexdigest()

    return reset_token, encrypted_token, expire_at
