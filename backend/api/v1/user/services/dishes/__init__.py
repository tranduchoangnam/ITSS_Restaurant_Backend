from .listing_dishes_service import listing_dishes, listing_suggested_dishes
from .create_dish_service import create_dish, create_dish_bulk
from .update_dish_service import update_dish
from .get_dish_detail_service import get_dish_detail
from .delete_dish_service import delete_dish
all = (
    listing_dishes,
    create_dish,
    create_dish_bulk,
    update_dish,
    get_dish_detail,
    listing_suggested_dishes
)


