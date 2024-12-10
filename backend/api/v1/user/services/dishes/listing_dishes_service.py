from datetime import datetime

from sqlalchemy import Date, case, literal, or_, any_
from sqlmodel import Session, String, cast, func, select
from sqlalchemy.sql.expression import func as sql_func

from backend.constants.account_status import AccountStatus
from backend.models.dish import Dish
from backend.models.user import User
from backend.schemas.dish import FilteringDishesQueryParams, DishBase
from backend.api.v1.dependencies.authentication import get_current_user


def listing_dishes(db: Session, query_params: FilteringDishesQueryParams):
    conditions = _build_conditions(query_params)
    dishes = _get_dishes(db, query_params, conditions)
    total = _count_dishes(db, conditions)

    return dishes, total


def listing_suggested_dishes(
    db: Session, query_params: FilteringDishesQueryParams, current_user: User
):
    conditions = _build_conditions(query_params)
    dishes = _get_suggested_dishes(db, query_params, conditions, current_user)
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


def _get_suggested_dishes(
    db: Session,
    query_params: FilteringDishesQueryParams,
    conditions: list,
    current_user: User,
):
    # Add conditions based on user preferences
    if current_user.loved_flavor:
        conditions.append(
            or_(
                func.lower(Dish.info).contains(current_user.loved_flavor.lower()),
                func.lower(current_user.loved_flavor)
                == any_(func.lower(Dish.categories)),
            )
        )

    if current_user.hated_flavor:
        conditions.append(
            ~or_(
                func.lower(Dish.info).contains(current_user.hated_flavor.lower()),
                func.lower(current_user.hated_flavor)
                == any_(func.lower(Dish.categories)),
            )
        )

    # if current_user.loved_distinct:
    #     conditions.append(
    #         func.lower(Dish.distinct).contains(current_user.loved_distinct.lower())
    #     )

    if current_user.loved_price:
        conditions.append(Dish.price <= current_user.loved_price)

    query = (
        select(Dish)
        .where(*conditions)
        .group_by(Dish.id)
        .limit(query_params.per_page)
        .offset((query_params.page - 1) * query_params.per_page)
    )

    dishes = db.exec(query).all()

    if len(dishes) < query_params.per_page:
        remaining_count = query_params.per_page - len(dishes)
        random_dishes = _get_random_dishes(
            db=db,
            exclude_ids=[
                dish.id for dish in dishes
            ],  # Exclude already suggested dishes
            limit=remaining_count,
        )
        dishes.extend([DishBase(**dish.model_dump()) for dish in random_dishes])

    return [DishBase(**dish.model_dump()) for dish in dishes]


def _get_random_dishes(db: Session, exclude_ids: list[int], limit: int):
    """
    Lấy các món ngẫu nhiên từ cơ sở dữ liệu, loại trừ các món đã được chọn trước đó.
    """
    query = (
        select(Dish)
        .where(~Dish.id.in_(exclude_ids))  # Loại trừ các món đã được chọn
        .order_by(sql_func.random())  # Lấy ngẫu nhiên
        .limit(limit)
    )

    return db.exec(query).all()


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
