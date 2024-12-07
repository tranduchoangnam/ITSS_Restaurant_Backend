from datetime import datetime

from sqlalchemy import Date, case, literal, or_, any_
from sqlmodel import Session, String, cast, func, select

from backend.constants.account_status import AccountStatus
from backend.models.dish import Dish
from backend.schemas.dish import FilteringDishesQueryParams, DishBase


def listing_dishes(db: Session, query_params: FilteringDishesQueryParams):
    conditions = _build_conditions(query_params)
    dishes = _get_dishes(db, query_params, conditions)
    total = _count_dishes(db, conditions)

    return dishes, total


def _get_dishes(
    db: Session, query_params: FilteringDishesQueryParams, conditions: list
):

    query = (
        select(Dish)
        .where(*conditions)
        .group_by(Dish.id)
        .limit(query_params.per_page)
        .offset((query_params.page - 1) * query_params.per_page)
    )

    dishes = db.exec(query).all()

    return [DishBase(**dish.model_dump()) for dish in dishes]


def _count_dishes(db: Session, conditions: list):
    query = select(func.count(Dish.id)).where(*conditions)
    total = db.exec(query).first()
    return total


def _build_conditions(query_params: FilteringDishesQueryParams):
    conditions = []

    if query_params.name_keyword:
        name_keyword = query_params.name_keyword.lower()
        conditions.append(
            or_(
                cast(Dish.id, String).contains(name_keyword),
                func.lower(Dish.name).contains(name_keyword),
                func.lower(Dish.address).contains(name_keyword),
                func.lower(Dish.price).contains(name_keyword),
                func.lower(Dish.info).contains(name_keyword),
                func.lower(name_keyword) == any_(func.lower(Dish.categories)),
            )
        )

    return conditions
