import json
from http import HTTPStatus

import pydantic
from flask import url_for

from tests.functional.settings import test_settings
from users_actions_app.api.v1.models.movie_rating import LikeDislike
from users_actions_app.init_db import mongodb_client


class TestMovieRating:
    def test_movie_rating_get(
        self, test_client, token_access_headers, movie_ratings, movie_uuid
    ):
        url = url_for("movie_rating.movie_rating", movie_id=movie_uuid)
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


class TestMovieRatingDelete:
    def test_movie_rating_post(
            self, test_client, token_access_headers, movie_uuid
    ):
        url = url_for("movie_rating.movie_rating")
        method = "post"
        data = {"movie_id": str(movie_uuid), "rating": 10}
        status = HTTPStatus.CREATED
        before_creation_count = mongodb_client[test_settings.db_name][
            test_settings.movie_rating_collection
        ].count_documents({"movie_id": str(movie_uuid)})
        response = getattr(test_client, method)(
            url, json=data, headers=token_access_headers
        )
        after_creation_count = mongodb_client[test_settings.db_name][
            test_settings.movie_rating_collection
        ].count_documents({"movie_id": str(movie_uuid)})
        assert response.status_code == status
        assert before_creation_count + 1 == after_creation_count

    def test_movie_rating_delete(
        self, test_client, token_access_headers, movie_rating, user_uuid
    ):
        url = url_for("movie_rating.delete", movie_id=movie_rating.movie_id)
        method = "delete"
        status = HTTPStatus.NO_CONTENT
        before_creation_count_reviews = mongodb_client[test_settings.db_name][
            test_settings.movie_rating_collection
        ].count_documents(
            {"movie_id": movie_rating.movie_id, "user_id": str(user_uuid)}
        )
        response = getattr(test_client, method)(
            url, headers=token_access_headers
        )
        after_creation_count_reviews = mongodb_client[test_settings.db_name][
            test_settings.movie_rating_collection
        ].count_documents(
            {"movie_id": movie_rating.movie_id, "user_id": str(user_uuid)}
        )
        assert response.status_code == status
        assert (
                before_creation_count_reviews - 1 ==
                after_creation_count_reviews
        )
