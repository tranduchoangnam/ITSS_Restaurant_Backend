from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from backend.models.review import Review
from backend.schemas.base import BaseResponse

class ReviewBase(BaseModel):
    id: Optional[int]
    user_id: Optional[int]
    dish_id: Optional[int]
    rating: Optional[int]
    comment: Optional[str]
    created_at: Optional[datetime]

class CreateReviewRequest(BaseModel):
    user_id: int
    dish_id: int
    rating: int
    comment: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": 1,
                    "dish_id": 1,
                    "rating": 5,
                    "comment": "Rat ngon ma khong so nong",
                }
            ]
        }
    }

class ListingDishReviewsResponse(BaseModel):
    avg_rating: float
    total: int
    reviews: List[ReviewBase]