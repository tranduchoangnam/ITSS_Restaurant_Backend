from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from backend.core.exception import BadRequestException, AccessDeniedException
from backend.core.error_code import ErrorCode, ErrorMessage
from backend.models.user import User, RoleCode
from backend.schemas.user import UpdateUserRequest, UserBaseResponse


def update_user(
    db: Session,
    current_user: User,
    request: UpdateUserRequest,
    user_id: int,
) -> UserBaseResponse:
    # Check if the user exists
    try:
        user = db.query(User).filter(User.id == user_id).one()
    except NoResultFound:
        raise BadRequestException(
            ErrorCode.ERR_NOT_FOUND, ErrorMessage.ERR_USER_NOT_FOUND
        )

    # Check if the current user is authorized to update this user
    if (current_user.role_code == RoleCode.USER) and (current_user.id != user_id):
        raise AccessDeniedException(
            ErrorCode.ERR_ACCESS_DENIED, ErrorMessage.ERR_ACCESS_DENIED
        )

    # Update the user's fields based on the request
    update_data = request.model_dump()
    for key, value in update_data.items():
        setattr(user, key, value)

    # Commit changes to the database
    db.add(user)
    db.commit()
    db.refresh(user)

    # Return the updated user
    return UserBaseResponse(**user.model_dump())
