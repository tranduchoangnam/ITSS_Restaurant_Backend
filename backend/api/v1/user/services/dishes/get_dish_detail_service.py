from datetime import datetime

from sqlalchemy import Date, case, literal, or_, any_
from sqlmodel import Session, String, cast, func, select

from backend.models.dish import Dish
from backend.schemas.dish import FilteringDishesQueryParams, DishBase
from backend.core.exception import BadRequestException
from backend.core.error_code import ErrorCode, ErrorMessage
def get_dish_detail(db: Session, dish_id: int):
    dish = db.exec(
        select(Dish)
        .where(Dish.id == dish_id)
    ).first()
    print(dish)
    if not dish:
        raise BadRequestException(ErrorCode.ERR_NOT_FOUND, ErrorMessage.ERR_DISH_NOT_FOUND)
    return DishBase(**dish.model_dump())