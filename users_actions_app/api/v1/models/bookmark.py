from pydantic import BaseModel

from users_actions_app.api.v1.models.common import CreateAtMixin, IDMixin


class BookmarkValidate(BaseModel):
    movie_id: str


class BookmarkCreate(CreateAtMixin):
    movie_id: str
    user_id: str


class Bookmark(CreateAtMixin, IDMixin):
    movie_id: str
    user_id: str
