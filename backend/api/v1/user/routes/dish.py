from typing import Annotated

from fastapi import APIRouter, Depends, Body
from sqlmodel import Session
import backend.api.v1.user.services.dishes as dish_service
from backend.api.v1.dependencies.authentication import authorize_role, get_user_if_logged_in, get_current_user
from backend.core.response import authenticated_api_responses, public_api_responses
from backend.db.database import get_db
from backend.models.dish import Dish
from backend.models.user import RoleCode, User
from backend.schemas.dish import FilteringDishesQueryParams, ListingDishesResponse, CreateDishRequest, CreateDishBulkRequest, DishBase, UpdateDishRequest, ListingDishBase

router = APIRouter()

@router.post(
    "",
    response_model=DishBase,
    responses=authenticated_api_responses,
)
def create_dish(
    request: CreateDishRequest,
    db: Session = Depends(get_db),
    admin: Annotated[User, Depends(authorize_role(RoleCode.ADMIN))] = None,
):
    return dish_service.create_dish(db, **request.model_dump())

@router.post(
    "/bulk",
    response_model=ListingDishBase,
    responses=authenticated_api_responses,
)
def create_dish_bulk(
    request: CreateDishBulkRequest,
    db: Session = Depends(get_db),
    admin: Annotated[User, Depends(authorize_role(RoleCode.ADMIN))] = None,
):
    return dish_service.create_dish_bulk(db, **request.model_dump())
    
@router.get(
    "",
    response_model=ListingDishesResponse,
    responses=public_api_responses,
)
def listing_dishes(
    db: Session = Depends(get_db),
    query_params: Annotated[
        FilteringDishesQueryParams, Depends(FilteringDishesQueryParams)
    ] = None,
    user: Annotated[User, Depends(get_user_if_logged_in)] = None,
):
    dishes, total = dish_service.listing_dishes(db, query_params, user)

    return ListingDishesResponse(
        page=query_params.page,
        per_page=query_params.per_page,
        total=total,
        data=dishes,
    )
    
@router.get(
    "/suggest",
    response_model=ListingDishesResponse,
    responses=authenticated_api_responses,
)
def listing_suggested_dishes(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
    query_params: Annotated[
        FilteringDishesQueryParams, Depends(FilteringDishesQueryParams)
    ] = None,
):
    dishes, total = dish_service.listing_suggested_dishes(db, query_params, current_user)

    return ListingDishesResponse(
        page=query_params.page,
        per_page=query_params.per_page,
        total=total,
        data=dishes,
    )
    
@router.get(
    "/{dish_id}",
    response_model=DishBase,
    responses=authenticated_api_responses,
)
def get_dish_by_id(
    dish_id: int,
    db: Session = Depends(get_db),
):
    dish = dish_service.get_dish_detail(db, dish_id)

    return dish

@router.patch(
    "/{dish_id}", response_model=DishBase, responses=authenticated_api_responses
)
def update_dish(
    dish_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(authorize_role(RoleCode.ADMIN))],
    request: UpdateDishRequest
):
    return dish_service.update_dish(db, request, dish_id)

@router.delete(
    "/{dish_id}",
    responses=authenticated_api_responses,
)
def delete_dish(
    dish_id: int,
    db: Session = Depends(get_db),
    current_user: Annotated[User, Depends(authorize_role(RoleCode.ADMIN))] = None,
):
    return dish_service.delete_dish(db, dish_id)

