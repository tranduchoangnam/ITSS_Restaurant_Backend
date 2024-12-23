# create dish service
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime
from backend.models.dish import Dish
from backend.schemas.dish import UpdateDishRequest, DishBase
from backend.utils import add_commit_refresh_object
from backend.map.map_service import get_location
from sqlalchemy.exc import NoResultFound
from backend.core.exception import BadRequestException, AccessDeniedException
from backend.core.error_code import ErrorCode, ErrorMessage

def delete_dish(   
    db: Session,
    dish_id: int,
):
    # Check if the dish exists
    try:
        dish = db.query(Dish).filter(Dish.id == dish_id).one()
    except NoResultFound:
        raise BadRequestException(
            ErrorCode.ERR_NOT_FOUND, ErrorMessage.ERR_USER_NOT_FOUND
        )
    db.delete(dish)
    db.commit()

    return dish_id
