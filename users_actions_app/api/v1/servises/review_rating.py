from typing import Optional

from bson import ObjectId

from users_actions_app.api.v1.models.movie_rating import (
    LikeDislike, MovieRatingCreate
)
from users_actions_app.api.v1.models.review_rating import ReviewRatingCreate
from users_actions_app.init_db import mongodb_client
from users_actions_app.settings import app_settings


class ReviewRatingService:
    def __init__(self, fields=None, user_id=None, review_id=None):
        self.fields: Optional[dict] = self._get_fields(fields, user_id)
        self.dict: dict = dict()
        self.user_id: Optional[str] = user_id
        self.review_id: Optional[str] = review_id
        self.obj: MovieRatingCreate = self._create_base_obj()
        self.collection = mongodb_client[app_settings.db_name][
            app_settings.review_rating_collection
        ]

    @staticmethod
    def _get_fields(fields, user_id):
        if not isinstance(fields, dict):
            return
        fields["user_id"] = user_id
        return fields

    def _create_base_obj(self):
        if self.fields:
            obj = ReviewRatingCreate(**self.fields)
            self.dict = obj.dict()
            self.dict["review_id"] = ObjectId(self.dict["review_id"])
            return obj
        return None

    def save_obj_to_db(self):
        filter_obj = {
            "user_id": self.user_id,
            "review_id": ObjectId(self.dict.get("review_id", ""))
        }
        new_values = {
            "rating": self.dict["rating"], "create_at": self.dict["create_at"]
        }
        self.collection.update_one(
            filter_obj,
            {"$set": new_values},
            upsert=True
        )
        return self.collection.find_one(self.dict)

    def dell_obj(self):
        self.collection.delete_many(
            {"user_id": self.user_id, "review_id": self.review_id}
        )

    def get_rating_info(self):
        likes = self.collection.count_documents(
            {"rating": 10, "review_id": ObjectId(self.review_id)}
        )
        dislikes = self.collection.count_documents(
            {"rating": 1, "review_id": ObjectId(self.review_id)}
        )
        if likes + dislikes == 0:
            average_value = 0
        else:
            average_value = ((likes * 10) + dislikes) / (likes + dislikes)
        return LikeDislike(
            likes=likes,
            dislikes=dislikes,
            average_value=average_value,
        ).dict()
