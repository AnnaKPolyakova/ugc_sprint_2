import logging
from http import HTTPStatus

from flask import Blueprint, request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from spectree import Response

from users_actions_app.api.utils import authentication_required, get_json
from users_actions_app.api.v1.models.common import Status
from users_actions_app.api.v1.models.movie_rating import LikeDislike
from users_actions_app.api.v1.models.review_rating import (
    Review,
    ReviewRating,
    ReviewRatingValidate,
)
from users_actions_app.api.v1.servises.review_rating import ReviewRatingService
from users_actions_app.utils import action_app_doc

logger = logging.getLogger(__name__)

review_rating_api = Blueprint("review_rating", __name__)


class ReviewRatingAPI(MethodView):
    @action_app_doc.validate(
        tags=["review_rating"],
        query=Review,
        resp=Response(
            HTTP_200=(LikeDislike, "add/update review_rating"),
            HTTP_400=(Status, "Error"),
        ),
    )
    def get(self):
        logging.debug(
            "ReviewRatingAPI {name} start".format(name=self.get.__name__)
        )
        review_id = request.args.get("review_id", type=str)
        try:
            info = ReviewRatingService(review_id=review_id).get_rating_info()
        except Exception as error:
            logging.error("ReviewRatingAPI error: {error}".format(error=error))
            return {"status": False}, HTTPStatus.BAD_REQUEST
        logging.debug(
            "ReviewRatingAPI {name} end".format(name=self.get.__name__)
        )
        return info, HTTPStatus.OK

    @authentication_required
    @action_app_doc.validate(
        tags=["review_rating"],
        json=ReviewRatingValidate,
        resp=Response(
            HTTP_201=(ReviewRating, "add/update review_rating"),
            HTTP_400=(Status, "Error"),
        ),
    )
    @jwt_required()
    def post(self):
        logging.debug(
            "ReviewRatingAPI {name} start".format(name=self.post.__name__)
        )
        request_data = request.get_json()
        user_id = get_jwt_identity()
        try:
            obj = ReviewRatingService(request_data, user_id).save_obj_to_db()
        except Exception as error:
            logging.error("ReviewRatingAPI error: {error}".format(error=error))
            return {"status": False}, HTTPStatus.BAD_REQUEST
        obj_json = get_json(obj)
        logging.debug(
            "ReviewRatingAPI {name} end".format(name=self.post.__name__)
        )
        return obj_json, HTTPStatus.CREATED


@authentication_required
@review_rating_api.route("/<path:review_id>/", methods=["DELETE"])
@action_app_doc.validate(
    tags=["review_rating"],
    resp=Response(
        HTTP_204=(Status, "dell rating"), HTTP_400=(Status, "Error")
    ),
)
@jwt_required()
def delete(review_id):
    logging.debug(
        "ReviewRatingAPI {name} start".format(name=delete.__name__)
    )
    user_id = get_jwt_identity()
    try:
        ReviewRatingService(user_id=user_id, review_id=review_id).dell_obj()
    except Exception as error:
        logging.error("ReviewRatingAPI error: {error}".format(error=error))
        return {"status": False}, HTTPStatus.BAD_REQUEST
    logging.debug(
        "ReviewRatingAPI {name} end".format(name=delete.__name__)
    )
    return {"status": "ok"}, HTTPStatus.NO_CONTENT


review_rating_api.add_url_rule(
    "/", view_func=ReviewRatingAPI.as_view("review_rating")
)
