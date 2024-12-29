# create dish service
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime
from backend.models.dish import Dish
from backend.schemas.dish import CreateDishRequest, DishBase, ListingDishBase
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


def create_dish_bulk(db: Session, **kwargs):
    dishes = []
    for dish in kwargs.get("data", []):
        dish = Dish(
            **dish,
            location=get_location(dish.get("address", "")),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        dishes.append(dish)
    db.add_all(dishes)
    db.commit()
    return ListingDishBase(
        data=[DishBase(**dish.model_dump()) for dish in dishes], total=len(dishes)
    )
