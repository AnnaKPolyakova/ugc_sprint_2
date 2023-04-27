from typing import Optional

from pydantic import BaseModel, validator

from users_actions_app.api.v1.models.common import CreateAtMixin, IDMixin


class ReviewRatingValidate(BaseModel):
    review_id: str
    rating: int

    @validator("rating")
    def value_must_be_within_range(cls, value):  # noqa: WPS110, N805
        if value not in (0, 10):
            raise ValueError("value must be 1 or 10")
        return value


class ReviewRatingCreate(CreateAtMixin):
    user_id: Optional[str]
    review_id: str
    rating: int


class ReviewRating(CreateAtMixin, IDMixin):
    user_id: str
    review_id: str
    rating: int


class Review(BaseModel):
    review_id: str
