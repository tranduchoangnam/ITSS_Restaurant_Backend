from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from backend.core.error_code import ErrorCode, ErrorMessage
from backend.core.exception import BadRequestException
from backend.models.review import Review
from backend.schemas.review import ListingDishReviewsResponse, ReviewBase

def delete_review(db: Session, review_id: int):
    try:
        review = db.query(Review).filter(Review.id == review_id).first()
    except NoResultFound:
        raise BadRequestException(
            ErrorCode.ERR_NOT_FOUND, ErrorMessage.ERR_USER_NOT_FOUND
        )
    db.delete(review)
    db.commit()

    return review_id