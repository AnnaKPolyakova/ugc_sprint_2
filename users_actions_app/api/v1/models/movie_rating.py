from typing import Optional

from pydantic import BaseModel, validator

from users_actions_app.api.v1.models.common import CreateAtMixin, IDMixin


class MovieRatingValidate(BaseModel):
    movie_id: str
    rating: int

    @validator("rating")
    def value_must_be_within_range(cls, value):  # noqa: WPS110, N805
        if value not in (1, 10):
            raise ValueError("value must be 1 or 10")
        return value


class MovieRatingCreate(CreateAtMixin):
    movie_id: str
    rating: int
    user_id: Optional[str]


class MovieRating(CreateAtMixin, IDMixin):
    movie_id: str
    rating: int
    user_id: Optional[str]


class Movie(BaseModel):
    movie_id: str


class LikeDislike(BaseModel):
    likes: int
    dislikes: int
    average_value: int
