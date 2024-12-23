from datetime import datetime
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from sqlmodel import Session

from backend.api.v1.user.services.auth.get_user_service import get_user_by_email
from backend.core.config import settings
from backend.core.error_code import ErrorCode
from backend.core.exception import AccessDeniedException, UnauthorizedException
from backend.db.database import get_db
from backend.models.user import RoleCode, User

auth = HTTPBearer(
    scheme_name='Authorization',
    auto_error=False
)

def get_current_user(
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(auth)],
):
    if token:
        try:
            token_value = token.credentials
            
            payload = jwt.decode(
                token_value, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            email = payload.get("sub")
            if (
                email is None
                or not isinstance(email, str)
                or datetime.now().timestamp() > payload.get("exp")
            ):
                raise UnauthorizedException(error_code=ErrorCode.ERR_UNAUTHORIZED)
        except JWTError:
            raise UnauthorizedException(error_code=ErrorCode.ERR_UNAUTHORIZED)
        user = get_user_by_email(db, email, payload.get("role"))
        if not user:
            raise UnauthorizedException(error_code=ErrorCode.ERR_UNAUTHORIZED)
        return user
    raise UnauthorizedException(error_code=ErrorCode.ERR_UNAUTHORIZED)

def get_user_if_logged_in(
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(auth)],
):
    if token:
        return get_current_user(db, token)

    return None


def authorize_role(role: RoleCode):
    def wrapper(current_user: User = Depends(get_current_user)):
        if current_user.role_code != role:
            raise AccessDeniedException(error_code=ErrorCode.ERR_ACCESS_DENIED)
        return current_user

    return wrapper
