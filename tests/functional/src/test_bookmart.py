import json
from http import HTTPStatus

from flask import url_for

from tests.functional.conftest import OBJ_COUNT
from tests.functional.settings import test_settings
from users_actions_app.init_db import mongodb_client


class TestBookmark:
    def test_bookmark_get(
        self,
        test_client,
        user_uuid,
        token_access_headers,
        bookmarks,
    ):
        url = url_for("bookmark.bookmark")
        method = "get"
        status = HTTPStatus.OK
        response = getattr(test_client, method)(
            url, headers=token_access_headers
        )
        assert response.status_code == status.OK
        assert len(json.loads(response.data.decode("utf-8"))) == OBJ_COUNT

    def test_bookmark_post(
        self,
        test_client,
        movie_uuid,
        user_uuid,
        token_access_headers,
    ):
        url = url_for("bookmark.bookmark")
        method = "post"
        data = {"movie_id": movie_uuid}
        status = HTTPStatus.CREATED
        before_creation_count = mongodb_client[test_settings.db_name][
            test_settings.bookmark_collection
        ].count_documents({"user_id": str(user_uuid)})
        response = getattr(test_client, method)(
            url, json=data, headers=token_access_headers
        )
        after_creation_count = mongodb_client[test_settings.db_name][
            test_settings.bookmark_collection
        ].count_documents({"user_id": str(user_uuid)})
        assert response.status_code == status
        assert before_creation_count + 1 == after_creation_count

    def test_bookmark_delete(
        self, test_client, user_uuid, token_access_headers, bookmark
    ):
        url = url_for("bookmark.delete", movie_id=bookmark.movie_id)
        method = "delete"
        status = HTTPStatus.NO_CONTENT
        before_creation_count = mongodb_client[test_settings.db_name][
            test_settings.bookmark_collection
        ].count_documents({"user_id": str(user_uuid)})
        response = getattr(test_client, method)(
            url, headers=token_access_headers
        )
        after_creation_count = mongodb_client[test_settings.db_name][
            test_settings.bookmark_collection
        ].count_documents({"user_id": str(user_uuid)})
        assert response.status_code == status
        assert before_creation_count - 1 == after_creation_count
