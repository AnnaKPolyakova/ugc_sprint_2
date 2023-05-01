from typing import Optional

from users_actions_app.api.v1.models.movie_rating import (
    LikeDislike, MovieRatingCreate
)
from users_actions_app.init_db import mongodb_client
from users_actions_app.settings import app_settings


class MovieRatingService:
    def __init__(self, fields=None, user_id=None, movie_id=None):
        self.fields: Optional[dict] = self._get_fields(fields, user_id)
        self.dict: dict = dict()
        self.user_id: Optional[str] = user_id
        self.movie_id: Optional[str] = movie_id
        self.obj: MovieRatingCreate = self._create_base_obj()
        self.collection = mongodb_client[app_settings.db_name][
            app_settings.movie_rating_collection
        ]

    @staticmethod
    def _get_fields(fields, user_id):
        if not isinstance(fields, dict):
            return
        fields["user_id"] = user_id
        return fields

    def _create_base_obj(self):
        if self.fields:
            obj = MovieRatingCreate(**self.fields)
            self.dict = obj.dict()
            return obj
        return None

    def save_obj_to_db(self):
        data = self.dict
        filter_obj = {"user_id": self.user_id, "movie_id": data["movie_id"]}
        new_values = {"rating": data["rating"], "create_at": data["create_at"]}
        self.collection.update_one(
            filter_obj,
            {"$set": new_values},
            upsert=True
        )
        return self.collection.find_one(data)

    def find_rating(self, movie_id):
        return self.collection.find_one(
            {"user_id": self.user_id, "movie_id": movie_id}
        )

    def dell_obj(self):
        self.collection.delete_many(
            {"user_id": self.user_id, "movie_id": self.movie_id}
        )
        collection_review_db = mongodb_client[app_settings.db_name][
            app_settings.movie_review_collection
        ]
        filter_obj = {"user_id": self.user_id, "movie_id": self.movie_id}
        new_values = {"$set": {"rating_id": ""}}
        collection_review_db.update_one(filter_obj, new_values)

    def get_rating_info(self):
        likes = self.collection.count_documents(
            {"rating": 10, "movie_id": self.movie_id}
        )
        dislikes = self.collection.count_documents(
            {"rating": 1, "movie_id": self.movie_id}
        )
        return LikeDislike(
            likes=likes,
            dislikes=dislikes,
            average_value=((likes * 10) + dislikes) / (likes + dislikes),
        ).dict()
