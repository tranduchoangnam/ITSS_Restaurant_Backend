from sqlmodel import Session
from sqlalchemy import select

from backend.models.review import Review
from backend.schemas.review import ReviewBase

def get_dish_reviews(
    db: Session,
    dish_id: int,
):
    query = select(Review).where(Review.dish_id == dish_id)
    reviews = db.exec(query).scalars().all()

    total = len(reviews)
    avg_rating = sum(review.rating for review in reviews if review.rating is not None) / total if total > 0 else 0

    review_bases = [ReviewBase(**review.model_dump()) for review in reviews]

    return review_bases, total, avg_rating
