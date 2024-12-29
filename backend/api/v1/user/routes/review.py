from typing import Annotated
from urllib import response

from fastapi import APIRouter, Depends
from sqlmodel import Session
import backend.api.v1.user.services.reviews as review_service
from backend.api.v1.dependencies.authentication import authorize_role, get_user_if_logged_in
from backend.core.response import authenticated_api_responses, public_api_responses
from backend.db.database import get_db
from backend.models.user import RoleCode, User
from backend.schemas.review import CreateReviewRequest, ListingDishReviewsResponse, ReviewBase

router = APIRouter()

@router.get(
    "/dish/{dish_id}",
    response_model=ListingDishReviewsResponse,
    responses=public_api_responses,
)
def get_dish_reviews(
    dish_id: int,
    db: Session = Depends(get_db)
):
    response = review_service.get_dish_reviews(db, dish_id)
    return ListingDishReviewsResponse(
        total=response.total,
        reviews=response.reviews,
        avg_rating=response.avg_rating
    )


@router.post(
    "/dish/{dish_id}",
    response_model=ReviewBase,
    responses=authenticated_api_responses,
)
def create_review(
    request: CreateReviewRequest,
    db: Session = Depends(get_db),
    user: Annotated[User, Depends(get_user_if_logged_in)] = None,
):
    return review_service.create_dish_review(db, **request.model_dump())

@router.delete(
    "/{review_id}",
    responses=authenticated_api_responses,
)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: Annotated[User, Depends(authorize_role(RoleCode.ADMIN))] = None,
):
    return review_service.delete_review(db, review_id)
