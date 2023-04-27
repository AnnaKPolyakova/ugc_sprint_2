import logging
from http import HTTPStatus

from flask import Blueprint, request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from spectree import Response

from users_actions_app.api.utils import authentication_required, get_json
from users_actions_app.api.v1.models.common import SortBy, Status
from users_actions_app.api.v1.models.review import (
    MovieReview, MovieReviewValidate
)
from users_actions_app.api.v1.servises.review import MovieReviewService
from users_actions_app.utils import action_app_doc

logger = logging.getLogger(__name__)

review_api = Blueprint("review", __name__)


class ReviewAPI(MethodView):
    @authentication_required
    @action_app_doc.validate(
        tags=["user"],
        json=MovieReviewValidate,
        resp=Response(
            HTTP_201=(MovieReview, "add/update rating"),
            HTTP_400=(Status, "Error")
        ),
    )
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        logging.debug("ReviewAPI {name} start".format(name=self.post.__name__))
        request_data = request.get_json()
        request_data["user_id"] = user_id
        try:
            obj = MovieReviewService(request_data, user_id).save_obj_to_db()
        except Exception as error:
            logging.error("ReviewAPI error: {error}".format(error=error))
            return {"status": False}, HTTPStatus.BAD_REQUEST
        obj_json = get_json(obj)
        logging.debug("ReviewAPI {name} end".format(name=self.post.__name__))
        return obj_json, HTTPStatus.CREATED


class ReviewDetailAPI(MethodView):
    @authentication_required
    @action_app_doc.validate(
        tags=["review"],
        resp=Response(
            HTTP_204=(Status, "dell review"), HTTP_400=(Status, "Error")
        ),
    )
    @jwt_required()
    def delete(self, movie_id):
        logging.debug(
            "ReviewAPI {name} start".format(name=self.delete.__name__)
        )
        user_id = get_jwt_identity()
        try:
            MovieReviewService(user_id=user_id, movie_id=movie_id).dell_obj()
        except Exception as error:
            logging.error("ReviewAPI error: {error}".format(error=error))
            return {"status": False}, HTTPStatus.BAD_REQUEST
        logging.debug("ReviewAPI {name} end".format(name=self.delete.__name__))
        return {"status": "ok"}, HTTPStatus.NO_CONTENT

    @action_app_doc.validate(
        tags=["review"],
        query=SortBy,
    )
    def get(self, movie_id):
        logging.debug("ReviewAPI {name} start".format(name=self.get.__name__))
        try:
            objs = MovieReviewService(movie_id=movie_id).get_obj(
                dict(request.args)
            )
        except Exception as error:
            logging.error("ReviewAPI error: {error}".format(error=error))
            return {"status": False}, HTTPStatus.BAD_REQUEST
        logging.debug("ReviewAPI {name} end".format(name=self.get.__name__))
        return objs, HTTPStatus.OK


review_api.add_url_rule("/", view_func=ReviewAPI.as_view("review"))
review_api.add_url_rule(
    "/<path:movie_id>/", view_func=ReviewDetailAPI.as_view("review_detail")
)
