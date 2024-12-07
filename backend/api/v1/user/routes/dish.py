from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session
import backend.api.v1.user.services.dishes as dish_service
from backend.api.v1.dependencies.authentication import authorize_role
from backend.core.response import authenticated_api_responses
from backend.db.database import get_db
from backend.models.dish import Dish
from backend.models.user import RoleCode, User
from backend.schemas.dish import FilteringDishesQueryParams, ListingDishesResponse, CreateDishRequest, DishBase

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
    
@router.get(
    "",
    response_model=ListingDishesResponse,
    responses=authenticated_api_responses,
)
def listing_dishes(
    db: Session = Depends(get_db),
    query_params: Annotated[
        FilteringDishesQueryParams, Depends(FilteringDishesQueryParams)
    ] = None,
):
    dishes, total = dish_service.listing_dishes(db, query_params)

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


