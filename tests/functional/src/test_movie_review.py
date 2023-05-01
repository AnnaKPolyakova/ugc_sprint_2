import json
import uuid
from http import HTTPStatus

from flask import url_for

from tests.functional.conftest import OBJ_COUNT
from tests.functional.settings import test_settings
from users_actions_app.init_db import mongodb_client


class TestMovieRating:
    def test_movie_review_get(
        self, test_client, token_access_headers, movies_reviews, movie_uuid
    ):
        url = url_for("review.review_detail", movie_id=movie_uuid)
        method = "get"
        status = HTTPStatus.OK
        response = getattr(test_client, method)(
            url, headers=token_access_headers
        )
        assert response.status_code == status.OK
        assert len(json.loads(response.data.decode("utf-8"))) == OBJ_COUNT

    def test_movie_review_post(
        self,
        test_client,
        token_access_headers,
    ):
        url = url_for("review.review")
        method = "post"
        movie_id = str(uuid.uuid4())
        data = {"text": "text", "movie_id": movie_id, "rating": 10}
        status = HTTPStatus.CREATED
        before_creation_count = mongodb_client[test_settings.db_name][
            test_settings.movie_review_collection
        ].count_documents({"movie_id": movie_id})
        before_creation_count_ratings = mongodb_client[test_settings.db_name][
            test_settings.movie_rating_collection
        ].count_documents({"movie_id": movie_id})
        response = getattr(test_client, method)(
            url, json=data, headers=token_access_headers
        )
        after_creation_count = mongodb_client[test_settings.db_name][
            test_settings.movie_review_collection
        ].count_documents({"movie_id": movie_id})
        after_creation_count_ratings = mongodb_client[test_settings.db_name][
            test_settings.movie_rating_collection
        ].count_documents({"movie_id": movie_id})
        assert response.status_code == status
        assert before_creation_count + 1 == after_creation_count
        assert (
                before_creation_count_ratings + 1 ==
                after_creation_count_ratings
        )

    def test_movie_review_delete(
        self, test_client, user_uuid, token_access_headers, movie_review
    ):
        url = url_for("review.review_detail", movie_id=movie_review.movie_id)
        method = "delete"
        status = HTTPStatus.NO_CONTENT
        before_count_reviews = mongodb_client[test_settings.db_name][
            test_settings.movie_review_collection
        ].count_documents({"movie_id": movie_review.movie_id})
        response = getattr(test_client, method)(
            url, headers=token_access_headers
        )
        after_count_reviews = mongodb_client[test_settings.db_name][
            test_settings.movie_review_collection
        ].count_documents({"movie_id": movie_review.movie_id})
        assert response.status_code == status
        assert before_count_reviews - 1 == after_count_reviews
