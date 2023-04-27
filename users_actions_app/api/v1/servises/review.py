from typing import Optional

from pymongo import ASCENDING, DESCENDING

from users_actions_app.api.utils import get_json
from users_actions_app.api.v1.models.common import CreateAtMixin, IDMixin
from users_actions_app.api.v1.models.movie_rating import (
    MovieRating,
)
from users_actions_app.api.v1.models.review import MovieReviewCreate
from users_actions_app.api.v1.servises.movie_rating import MovieRatingService
from users_actions_app.init_db import mongodb_client
from users_actions_app.settings import app_settings

SORT = {"asc": ASCENDING, "des": DESCENDING}


class MovieReviewService:
    def __init__(self, fields=None, user_id=None, movie_id=None):
        self.fields: Optional[dict] = fields
        self.dict: dict = dict()
        self.user_id: Optional[dict] = user_id
        self.movie_id: Optional[movie_id] = movie_id
        self.obj: MovieReviewCreate = self._create_base_obj()
        self.collection = mongodb_client[app_settings.db_name][
            app_settings.movie_review_collection
        ]

    def _create_base_obj(self):
        if self.fields:
            obj = MovieReviewCreate(**self.fields)
            self.dict = obj.dict()
            return obj
        return None

    def save_obj_to_db(self):
        data = self.dict
        data["user_id"] = self.user_id
        if data.get("rating", None) is not None:
            obj = MovieRatingService(
                {
                    "rating": data.get("rating", None),
                    "movie_id": data.get("movie_id", None),
                },
                self.user_id,
            ).save_obj_to_db()
            data["rating_id"] = obj.get("_id", None)
        else:
            rating = MovieRatingService(user_id=self.user_id).find_rating(
                self.dict.get("movie_id", "")
            )
            if rating is not None:
                data["rating_id"] = rating.get("_id")
        del data["rating"]
        filter_obj = {
            "user_id": self.user_id, "movie_id": data.get("movie_id", None)
        }
        new_values = {
            "$set": {
                "rating_id": data.get("rating_id", None),
                "create_at": data.get("create_at", None),
                "text": data.get("text", None),
            }
        }
        result = self.collection.update_one(filter_obj, new_values)
        data["user_id"] = self.user_id
        if result.matched_count == 0:
            self.collection.insert_one(data)
        return self.collection.find_one(data)

    def dell_obj(self):
        review = list(
            self.collection.find(
                {"user_id": self.user_id, "movie_id": self.movie_id}
            )
        )
        reviews_ids = [str(obj.get("_id", "")) for obj in review]
        self.collection.delete_many(
            {"user_id": self.user_id, "movie_id": self.movie_id}
        )
        review_rating_collection = mongodb_client[app_settings.db_name][
            app_settings.review_rating_collection
        ]
        review_rating_collection.delete_many(
            {"user_id": self.user_id, "review_id": {"$in": reviews_ids}}
        )

    def get_obj(self, sort: dict):
        sort_field = sort.get("sort_field", "create_at")
        sort_by = DESCENDING
        if sort_field is not None:
            if sort_field.startswith("-"):
                sort_field = sort_field[1:]
            else:
                sort_by = ASCENDING
        if sort_field is not None and sort_field in MovieRating.__fields__:
            sort_agr = {
                "{from_collection}.{field}".format(
                    from_collection=app_settings.movie_rating_collection,
                    field=sort_field,
                ): sort_by
            }
        elif sort_field is not None and sort_field in MovieReview.__fields__:
            sort_agr = {"{field}".format(field=sort_field): sort_by}
        elif sort_field == "review_rating":
            sort_agr = {"avg_rating": sort_by}
        else:
            sort_agr = {"create_at": sort_by}
        pipeline = [
            {"$match": {"movie_id": self.movie_id}},
            {
                "$lookup": {
                    "from": app_settings.movie_rating_collection,
                    "localField": "rating_id",
                    "foreignField": "_id",
                    "as": app_settings.movie_rating_collection,
                }
            },
            {
                "$lookup": {
                    "from": app_settings.review_rating_collection,
                    "localField": "_id",
                    "foreignField": "review_id",
                    "as": app_settings.review_rating_collection,
                }
            },
            {
                "$addFields": {
                    "avg_rating": {
                        "$avg": "${review_rating}.rating".format(
                            review_rating=app_settings.review_rating_collection
                        )
                    }
                }
            },
            {"$sort": sort_agr},
        ]
        objs = self.collection.aggregate(pipeline)
        return get_json(list(objs))


class MovieReview(CreateAtMixin, IDMixin):
    text: str
    user_id: str
    rating_id: Optional[str] = None
