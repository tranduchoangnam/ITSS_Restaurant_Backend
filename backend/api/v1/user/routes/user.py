from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path
from sqlmodel import Session

import backend.api.v1.user.services.users as users_service

# from backend.api.v1.dependencies.authentication import get_current_audience
from backend.api.v1.dependencies.authentication import authorize_role, get_user_if_logged_in
from backend.core.response import authenticated_api_responses, public_api_responses
from backend.db.database import get_db
from backend.models.user import RoleCode, User
from backend.schemas.auth import GetMeResponse, TokenResponse
from backend.schemas.user import (
    InputRegisterUserRequest,
    UpdateUserPublicInformationRequest,
    UpdateUserRequest,
    UserBaseResponse,
)

router = APIRouter()


# @router.post("/register", response_model=EmailVerifyTokenResponse)
# async def register(
#     request: RegisterAudienceRequest,
#     db: Session = Depends(get_db),
# ):
#     new_user = await users_service.register_first_step(db, request.email)
#     return EmailVerifyTokenResponse(
#         email=new_user.email, expire_at=new_user.email_verify_token_expire_at
#     )


# @router.patch(
#     "/public-information",
#     response_model=GetMeResponse,
#     responses=authenticated_api_responses,
# )
# def update_user_public_information(
#     db: Annotated[Session, Depends(get_db)],
#     current_user: Annotated[User, Depends(authorize_role(RoleCode.USER))],
#     request: Annotated[
#         UpdateUserPublicInformationRequest,
#         Body(
#             title="Update User Public Information request",
#             description="Provide avatar_url, display_name",
#         ),
#     ],
# ):
#     return users_service.update_user_public_information(db, current_user, request)


@router.patch(
    "/{user_id}", response_model=UserBaseResponse, responses=authenticated_api_responses
)
def update_user(
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_user_if_logged_in)],
    request: Annotated[
        UpdateUserRequest,
        Body(
            title="Update User Request",
            description="Provide all required user information",
        ),
    ],
):
    return users_service.update_user(db, current_user, request, user_id)


# @router.delete(
#     "/{user_id}",
#     status_code=HTTPStatus.NO_CONTENT,
#     responses=authenticated_api_responses,
# )
# def delete_user(
#     user_id: int,
#     db: Annotated[Session, Depends(get_db)],
#     current_user: Annotated[User, Depends(authorize_role(RoleCode.USER))],
# ):
#     return users_service.delete_user(db, current_user, user_id)

