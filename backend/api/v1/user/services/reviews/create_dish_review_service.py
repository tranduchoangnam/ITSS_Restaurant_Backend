from backend.models.review import Review
from backend.utils import add_commit_refresh_object
from sqlalchemy.orm import Session
from datetime import datetime


def create_dish_review(db: Session, **kwargs):
    review = Review(**kwargs,
                    created_at=datetime.now(),
                    updated_at=datetime.now())

    add_commit_refresh_object(db, review)
    return Review(**review.model_dump())