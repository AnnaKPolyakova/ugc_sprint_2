import logging
import uuid
from http import HTTPStatus
from unittest.mock import patch

import pytest
from flask import Blueprint
from flask_jwt_extended import JWTManager, create_access_token

from tests.functional.settings import TestSettings, test_settings
from tests.functional.utils.factories import (
    BookmarkFactory,
    MovieRatingFactory,
    MovieReviewFactory,
    ReviewRatingFactory,
)
from tests.functional.utils.mock import mock_authentication_required_decorator

OBJ_COUNT = 2
TEST_FOR_TOKEN = "test_for_token"

ERROR_INFO = (
    "Проверьте, что при {method} запросе {url} возвращается статус {status}"
)

patch(
    "users_actions_app.api.utils.authentication_required",
    mock_authentication_required_decorator,
).start()
patch("users_actions_app.settings.app_settings", return_value=TestSettings())


@pytest.fixture(scope="session", autouse=True)
def test_db():
    from users_actions_app.init_db import mongodb_client

    try:
        db = mongodb_client[test_settings.db_name]
    except Exception as error:
        logging.error(error)
    else:
        yield db
        mongodb_client.drop_database(test_settings.db_name)


@pytest.fixture(scope="session", autouse=True)
def test_app(test_db):
    from users_actions_app.action_app import create_action_app
    app = create_action_app(test_settings)
    app.config["SERVER_NAME"] = "localhost"
    app.config["TESTING"] = True
    auth_api = Blueprint("auth", __name__)

    @auth_api.route("/", methods=["GET"])
    def auth():
        return {}, HTTPStatus.OK

    app.register_blueprint(auth_api, url_prefix="/api/v1/auth")
    yield app


@pytest.fixture(scope="session", autouse=True)
def test_jwt(test_app):
    yield JWTManager(test_app)


@pytest.fixture(scope="session")
def user_uuid():
    return uuid.uuid4()


@pytest.fixture(scope="session")
def movie_uuid():
    return uuid.uuid4()


@pytest.fixture(scope="session")
def test_client(test_db, test_app):
    with test_app.test_client() as testing_client:
        with test_app.app_context():
            yield testing_client


@pytest.fixture(scope="function")
def movie_ratings(test_db, test_app, movie_uuid):
    return MovieRatingFactory.create_batch(OBJ_COUNT, movie_id=str(movie_uuid))


@pytest.fixture(scope="function")
def movie_rating(test_db, test_app, user_uuid):
    return MovieRatingFactory(user_id=str(user_uuid))


@pytest.fixture(scope="function")
def bookmarks(test_db, test_app, user_uuid):
    return BookmarkFactory.create_batch(OBJ_COUNT, user_id=str(user_uuid))


@pytest.fixture(scope="function")
def bookmark(test_db, test_app, user_uuid):
    return BookmarkFactory(user_id=str(user_uuid))


@pytest.fixture()
def token_access_headers(test_db, test_app, user_uuid):
    access_token = create_access_token(identity=str(user_uuid))
    return {
        "Authorization": "Bearer {access_token}".format(
            access_token=access_token
        )
    }


@pytest.fixture(scope="function")
def movies_reviews(test_db, test_app, movie_uuid):
    return MovieReviewFactory.create_batch(OBJ_COUNT, movie_id=str(movie_uuid))


@pytest.fixture(scope="function")
def movie_review(test_db, test_app, user_uuid):
    return MovieReviewFactory(user_id=str(user_uuid))


@pytest.fixture(scope="function")
def reviews_ratings(test_db, test_app, movie_review):
    return ReviewRatingFactory.create_batch(
        OBJ_COUNT, review_id=movie_review.id
    )


@pytest.fixture(scope="function")
def review_rating(test_db, test_app, movie_review):
    return ReviewRatingFactory(review_id=movie_review.id)
