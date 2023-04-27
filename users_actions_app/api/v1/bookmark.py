import logging
from http import HTTPStatus

from flask import Blueprint, request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from spectree import Response

from users_actions_app.api.utils import authentication_required, get_json
from users_actions_app.api.v1.models.bookmark import Bookmark, BookmarkValidate
from users_actions_app.api.v1.models.common import Status
from users_actions_app.api.v1.servises.bookmark import BookmarkService
from users_actions_app.utils import action_app_doc

logger = logging.getLogger(__name__)

bookmark_api = Blueprint("bookmark", __name__)


class BookmarkAPI(MethodView):
    @authentication_required
    @action_app_doc.validate(
        tags=["bookmark"],
    )
    @jwt_required()
    def get(self):
        logging.debug(
            "BookmarkAPI {name} start".format(name=self.get.__name__)
        )
        user_id = get_jwt_identity()
        try:
            info = BookmarkService(user_id=user_id).get_users_bookmark()
        except Exception as error:
            logging.error("BookmarkAPI error: {error}".format(error=error))
            return {"status": False}, HTTPStatus.BAD_REQUEST
        logging.debug(
            "BookmarkAPI {name} end".format(name=self.get.__name__)
        )
        return info, HTTPStatus.OK

    @authentication_required
    @action_app_doc.validate(
        tags=["bookmark"],
        json=BookmarkValidate,
        resp=Response(
            HTTP_201=(Bookmark, "add bookmark"),
            HTTP_400=(Status, "Error")
        ),
    )
    @jwt_required()
    def post(self):
        logging.debug(
            "BookmarkAPI {name} start".format(name=self.post.__name__)
        )
        request_data = request.get_json()
        user_id = get_jwt_identity()
        try:
            obj = BookmarkService(request_data, user_id).save_obj_to_db()
        except Exception as error:
            logging.error("BookmarkAPI error: {error}".format(error=error))
            return {"status": False}, HTTPStatus.BAD_REQUEST
        obj_json = get_json(obj)
        logging.debug(
            "BookmarkAPI {name} end".format(name=self.post.__name__)
        )
        return obj_json, HTTPStatus.CREATED


@authentication_required
@bookmark_api.route("/<path:movie_id>/", methods=["DELETE"])
@action_app_doc.validate(
    tags=["bookmark"],
    resp=Response(
        HTTP_204=(Status, "dell rating"), HTTP_400=(Status, "Error")
    ),
)
@jwt_required()
def delete(movie_id):
    logging.debug("BookmarkAPI {name} start".format(name=delete.__name__))
    user_id = get_jwt_identity()
    try:
        BookmarkService(user_id=user_id, movie_id=movie_id).dell_obj()
    except Exception as error:
        logging.error("BookmarkAPI error: {error}".format(error=error))
        return {"status": False}, HTTPStatus.BAD_REQUEST
    logging.debug("BookmarkAPI {name} end".format(name=delete.__name__))
    return {"status": "ok"}, HTTPStatus.NO_CONTENT


bookmark_api.add_url_rule("/", view_func=BookmarkAPI.as_view("bookmark"))
