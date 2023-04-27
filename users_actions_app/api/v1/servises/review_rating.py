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
        self.fields: Optional[dict] = fields
        self.dict: dict = dict()
        self.user_id: Optional[str] = user_id
        self.review_id: Optional[str] = review_id
        self.obj: MovieRatingCreate = self._create_base_obj()
        self.collection = mongodb_client[app_settings.db_name][
            app_settings.review_rating_collection
        ]

    def _create_base_obj(self):
        if self.fields:
            obj = ReviewRatingCreate(**self.fields)
            self.dict = obj.dict()
            return obj
        return None

    def save_obj_to_db(self):
        data = self.dict
        filter_obj = {
            "user_id": self.user_id,
            "review_id": data.get("review_id", "")
        }
        new_values = {
            "$set": {"rating": data["rating"], "create_at": data["create_at"]}
        }
        result = self.collection.update_one(filter_obj, new_values)
        data["user_id"] = self.user_id
        data["review_id"] = ObjectId(data["review_id"])
        if result.matched_count == 0:
            self.collection.insert_one(data)
        return self.collection.find_one(data)

    def dell_obj(self):
        self.collection.delete_many(
            {"user_id": self.user_id, "review_id": self.review_id}
        )

    def get_rating_info(self):
        likes = self.collection.count_documents(
            {"rating": 10, "review_id": self.review_id}
        )
        dislikes = self.collection.count_documents(
            {"rating": 1, "review_id": self.review_id}
        )
        return LikeDislike(
            likes=likes,
            dislikes=dislikes,
            average_value=((likes * 10) + dislikes) / (likes + dislikes),
        ).dict()
