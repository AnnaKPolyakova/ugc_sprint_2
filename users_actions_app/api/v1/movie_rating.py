import logging
from http import HTTPStatus

from flask import Blueprint, request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from spectree import Response

from users_actions_app.api.utils import authentication_required, get_json
from users_actions_app.api.v1.models.common import Status
from users_actions_app.api.v1.models.movie_rating import (
    LikeDislike,
    Movie,
    MovieRating,
    MovieRatingValidate,
)
from users_actions_app.api.v1.servises.movie_rating import MovieRatingService
from users_actions_app.utils import action_app_doc

logger = logging.getLogger(__name__)

movie_rating_api = Blueprint("movie_rating", __name__)


class MovieRatingAPI(MethodView):
    @action_app_doc.validate(
        tags=["movie_rating"],
        query=Movie,
        resp=Response(
            HTTP_200=(LikeDislike, "add/update rating"),
            HTTP_400=(Status, "Error")
        ),
    )
    def get(self):
        logging.debug(
            "MovieRatingAPI {name} start".format(name=self.get.__name__)
        )
        movie_id = request.args.get("movie_id", type=str)
        try:
            info = MovieRatingService(movie_id=movie_id).get_rating_info()
        except Exception as error:
            logging.error("MovieRatingAPI error: {error}".format(error=error))
            return {"status": False}, HTTPStatus.BAD_REQUEST
        logging.debug(
            "MovieRatingAPI {name} end".format(name=self.get.__name__)
        )
        return info, HTTPStatus.OK

    @authentication_required
    @action_app_doc.validate(
        tags=["movie_rating"],
        json=MovieRatingValidate,
        resp=Response(
            HTTP_201=(MovieRating, "add/update movie_rating"),
            HTTP_400=(Status, "Error"),
        ),
    )
    @jwt_required()
    def post(self):
        logging.debug(
            "MovieRatingAPI {name} start".format(name=self.post.__name__)
        )
        request_data = request.get_json()
        user_id = get_jwt_identity()
        try:
            obj = MovieRatingService(request_data, user_id).save_obj_to_db()
        except Exception as error:
            logging.error("MovieRatingAPI error: {error}".format(error=error))
            return {"status": False}, HTTPStatus.BAD_REQUEST
        obj_json = get_json(obj)
        logging.debug(
            "MovieRatingAPI {name} end".format(name=self.post.__name__)
        )
        return obj_json, HTTPStatus.CREATED


@authentication_required
@movie_rating_api.route("/<path:movie_id>/", methods=["DELETE"])
@action_app_doc.validate(
    tags=["movie_rating"],
    resp=Response(
        HTTP_204=(Status, "dell movie_rating"), HTTP_400=(Status, "Error")
    ),
)
@jwt_required()
def delete(movie_id):
    logging.debug(
        "MovieRatingAPI {name} start".format(name=delete.__name__)
    )
    user_id = get_jwt_identity()
    try:
        MovieRatingService(user_id=user_id, movie_id=movie_id).dell_obj()
    except Exception as error:
        logging.error("MovieRatingAPI error: {error}".format(error=error))
        return {"status": False}, HTTPStatus.BAD_REQUEST
    logging.debug(
        "MovieRatingAPI {name} end".format(name=delete.__name__)
    )
    return {"status": "ok"}, HTTPStatus.NO_CONTENT


movie_rating_api.add_url_rule(
    "/", view_func=MovieRatingAPI.as_view("movie_rating")
)
