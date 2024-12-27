
from .create_dish_review_service import create_dish_review
from .get_dish_reviews_service import get_dish_reviews
from .delete_review_service import delete_review

all = (
    create_dish_review,
    get_dish_reviews,
    delete_review
)