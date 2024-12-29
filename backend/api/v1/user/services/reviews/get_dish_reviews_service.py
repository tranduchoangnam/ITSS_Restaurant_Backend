from sqlmodel import Session
from sqlalchemy import select

from backend.models.review import Review
from backend.models.user import User
from backend.schemas.review import ListingDishReviewsResponse, ReviewBase

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
        tmp_review['display_name'] = user.display_name
        tmp_review['avatar_url'] = user.avatar_url
        review_bases.append(ReviewBase(**tmp_review))

    return ListingDishReviewsResponse(
        total=total,
        reviews=review_bases,
        avg_rating=avg_rating,
    )