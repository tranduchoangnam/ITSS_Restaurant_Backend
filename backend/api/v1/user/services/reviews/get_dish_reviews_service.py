from sqlmodel import Session
from sqlalchemy import select

from backend.models.review import Review
from backend.models.user import User
from backend.schemas.review import ReviewBase

def get_dish_reviews(
    db: Session,
    dish_id: int,
):
    query = select(Review).where(Review.dish_id == dish_id)
    reviews = db.exec(query).scalars().all()

    total = len(reviews)
    avg_rating = sum(review.rating for review in reviews if review.rating is not None) / total if total > 0 else 0

    review_bases = []
    for review in reviews:
        queryUser = select(User).where(User.id == review.user_id)
        user = db.exec(queryUser).scalars().first()
        tmp_review = review.model_dump()
        tmp_review['user_name'] = user.display_name
        tmp_review['user_avatar_url'] = user.avatar_url
        review_bases.append(ReviewBase(**tmp_review))

    return review_bases, total, avg_rating