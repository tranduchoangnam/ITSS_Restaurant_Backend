# create dish service
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime
from backend.models.dish import Dish
from backend.schemas.dish import CreateDishRequest, DishBase
from backend.utils import add_commit_refresh_object
from backend.map.map_service import get_location


def create_dish(db: Session, **kwargs):
    dish = Dish(
        **kwargs,
        location=get_location(kwargs.get("address", "")),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    add_commit_refresh_object(db, dish)
    return DishBase(**dish.model_dump())
