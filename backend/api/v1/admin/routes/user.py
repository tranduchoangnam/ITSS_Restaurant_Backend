from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

import backend.api.v1.admin.services.users as user_service
from backend.api.v1.dependencies.authentication import authorize_role
from backend.core.response import authenticated_api_responses
from backend.db.database import get_db
from backend.models.user import RoleCode, User
from backend.schemas.user import FilteringUsersQueryParams, ListingUsersResponse

router = APIRouter()


@router.get(
    "",
    response_model=ListingUsersResponse,
    responses=authenticated_api_responses,
)
def listing_users(
    db: Session = Depends(get_db),
    admin: Annotated[User, Depends(authorize_role(RoleCode.ADMIN))] = None,
    query_params: Annotated[
        FilteringUsersQueryParams, Depends(FilteringUsersQueryParams)
    ] = None,
):
    users, total = user_service.listing_users(db, query_params)

    return ListingUsersResponse(
        page=query_params.page,
        per_page=query_params.per_page,
        total=total,
        data=users,
    )
