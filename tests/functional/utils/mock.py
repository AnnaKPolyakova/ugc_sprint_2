from functools import wraps

from flask import jsonify, request


def mock_authentication_required_decorator(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        headers = request.headers.environ
        if headers.get("HTTP_AUTHORIZATION", None):
            return func(*args, **kwargs)
        return jsonify({"info": "unauthorized access"}), 401

    return wrapped


def mock_mongodb_init(client, settings):
    return client[settings.db_name]
