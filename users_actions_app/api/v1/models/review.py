from typing import Optional

from pydantic import BaseModel

from users_actions_app.api.v1.models.common import CreateAtMixin, IDMixin


class MovieReviewValidate(BaseModel):
    text: str
    movie_id: str
    rating: Optional[int]


class MovieReviewCreate(CreateAtMixin):
    text: str
    movie_id: str
    rating: Optional[int]


class MovieReview(CreateAtMixin, IDMixin):
    text: str
    movie_id: str
    user_id: str
    rating_id: Optional[str] = None
