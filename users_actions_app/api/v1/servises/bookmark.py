from typing import Optional

from users_actions_app.api.utils import get_json
from users_actions_app.api.v1.models.bookmark import BookmarkCreate
from users_actions_app.init_db import mongodb_client
from users_actions_app.settings import app_settings


class BookmarkService:
    def __init__(self, fields=None, user_id=None, movie_id=None):
        self.fields: Optional[dict] = self._get_fields(fields, user_id)
        self.dict: dict = {}
        self.user_id: Optional[str] = user_id
        self.movie_id: Optional[str] = movie_id
        self.obj: BookmarkCreate = self._create_base_obj()
        self.collection = mongodb_client[app_settings.db_name][
            app_settings.bookmark_collection
        ]

    @staticmethod
    def _get_fields(fields, user_id):
        if not isinstance(fields, dict):
            return
        fields["user_id"] = user_id
        return fields

    def _create_base_obj(self):
        if self.fields:
            obj = BookmarkCreate(**self.fields)
            self.dict = obj.dict()
            return obj
        return None

    def save_obj_to_db(self):
        filter_obj = {
            "user_id": self.user_id, "movie_id": self.dict.get("movie_id", "")
        }
        self.collection.update_one(
            filter_obj,
            {"$set": {}},
            upsert=True
        )
        obj = self.collection.find_one(filter_obj)
        return obj

    def dell_obj(self):
        self.collection.delete_many(
            {"user_id": self.user_id, "movie_id": self.movie_id}
        )

    def get_users_bookmark(self):
        objs = self.collection.find({"user_id": self.user_id})
        return get_json(list(objs))
