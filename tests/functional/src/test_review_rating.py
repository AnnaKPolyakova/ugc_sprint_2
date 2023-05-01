import json
from http import HTTPStatus

import pydantic
from flask import url_for

from tests.functional.settings import test_settings
from users_actions_app.api.v1.models.movie_rating import LikeDislike
from users_actions_app.init_db import mongodb_client


class TestReviewRating:
    def test_review_rating_get(
        self, test_client, token_access_headers, reviews_ratings, movie_review
    ):
        url = url_for("review_rating.review_rating", review_id=movie_review.id)
        method = "get"
        status = HTTPStatus.OK
        response = getattr(test_client, method)(
            url, headers=token_access_headers
        )
        data = json.loads(response.data.decode("utf-8"))
        assert response.status_code == status.OK
        try:
            LikeDislike(**data)
        except pydantic.ValidationError:
            assert "Схема ответа" == data

    def test_review_rating_post(
            self, test_client, token_access_headers, movie_review
    ):
        url = url_for("review_rating.review_rating")
        method = "post"
        data = {"review_id": str(movie_review.id), "rating": 10}
        status = HTTPStatus.CREATED
        before_creation_count = mongodb_client[test_settings.db_name][
            test_settings.review_rating_collection
        ].count_documents({"review_id": movie_review.id})
        response = getattr(test_client, method)(
            url, json=data, headers=token_access_headers
        )
        after_creation_count = mongodb_client[test_settings.db_name][
            test_settings.review_rating_collection
        ].count_documents({"review_id": movie_review.id})
        assert response.status_code == status
        assert before_creation_count + 1 == after_creation_count

    def test_review_rating_delete(
        self, test_client, token_access_headers, review_rating, movie_review
    ):
        url = url_for("review_rating.delete", review_id=review_rating.id)
        method = "delete"
        status = HTTPStatus.NO_CONTENT
        before_creation_count_reviews = mongodb_client[test_settings.db_name][
            test_settings.review_rating_collection
        ].count_documents({"review_id": movie_review.id})
        response = getattr(test_client, method)(
            url, headers=token_access_headers
        )
        after_creation_count_reviews = mongodb_client[test_settings.db_name][
            test_settings.review_rating_collection
        ].count_documents({"movie_id": movie_review.id})
        assert response.status_code == status
        assert (
                before_creation_count_reviews - 1 ==
                after_creation_count_reviews
        )
