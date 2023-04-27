import json
from datetime import datetime
from functools import wraps
from http import HTTPStatus
from typing import Union

import requests
from bson import ObjectId
from flask import jsonify, request

from users_actions_app.settings import app_settings


def authentication_required(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        headers = request.headers.environ
        authorization = headers.get("HTTP_AUTHORIZATION", None)
        response = getattr(requests, "get")(
            app_settings.auth_host,
            headers={
                "Authorization": authorization,
            },
        )
        if response.status_code != HTTPStatus.OK:
            return jsonify({"info": "unauthorized access"}), 401
        return func(*args, **kwargs)

    return wrapped


class AppJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)


def get_json(obj: Union[dict, list]):
    json_document_str = json.dumps(obj, cls=AppJSONEncoder)
    return json.loads(json_document_str)
