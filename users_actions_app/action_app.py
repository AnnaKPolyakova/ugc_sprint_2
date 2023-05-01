import datetime as dt
import json
import logging
from logging.config import dictConfig
from os import makedirs

import sentry_sdk
from flask import Flask, request
from flask_jwt_extended import JWTManager

from users_actions_app.api.v1.bookmark import bookmark_api
from users_actions_app.api.v1.movie_rating import movie_rating_api
from users_actions_app.api.v1.review import review_api
from users_actions_app.api.v1.review_rating import review_rating_api
from users_actions_app.init_db import mongodb_client, mongodb_init
from users_actions_app.settings import app_settings
from users_actions_app.utils import action_app_doc

sentry_sdk.init(dsn=app_settings.dsn, traces_sample_rate=1.0)


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log = {
            "time": str(dt.datetime.fromtimestamp(record.created)),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "request_id": getattr(record, "request_id", "")
        }
        return json.dumps(log)


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        if request:
            record.request_id = request.headers.get("X-Request-Id", "")
        return True


def create_action_app(settings):
    log_dir = settings.log_dir
    log_file = log_dir + settings.log_file
    makedirs(log_dir, exist_ok=True)
    dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                '()': 'users_actions_app.action_app.JsonFormatter',
            },
            "simple": {
                "format": "%(asctime)s - %(message)s",
            },
        },
        'filters': {
            'app_filter': {
                '()': RequestIdFilter,
            },
        },
        'handlers': {
            'file': {
                'class': 'logging.FileHandler',
                'filename': log_file,
                'level': settings.log_level,
                'formatter': 'standard',
                'filters': ['app_filter'],
            },
            'console':
                {
                    "class": "logging.StreamHandler",
                    'level': settings.log_level,
                    'formatter': 'simple',
                }
        },
        'root': {
            'handlers': ['file', 'console'],
        },
        'loggers': {
            '': {
                'handlers': ['file'],
                'level': settings.log_level,
                'propagate': True,
            },
        },
    })
    current_app = Flask(__name__)
    current_app.register_blueprint(
        movie_rating_api, url_prefix="/api/v1/movie_rating"
    )
    current_app.register_blueprint(
        review_rating_api, url_prefix="/api/v1/review_rating"
    )
    current_app.register_blueprint(review_api, url_prefix="/api/v1/review")
    current_app.register_blueprint(bookmark_api, url_prefix="/api/v1/bookmark")
    action_app_doc.register(current_app)
    current_app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    current_app.config["JWT_HEADER_NAME"] = "Authorization"
    current_app.config["JWT_HEADER_TYPE"] = "Bearer"
    current_app.config["JWT_SECRET_KEY"] = settings.jwt_secret_key
    JWTManager(current_app)
    mongodb_init(mongodb_client, settings)
    return current_app


if __name__ == "__main__":
    app = create_action_app(app_settings)
    app.run(port=5000)
