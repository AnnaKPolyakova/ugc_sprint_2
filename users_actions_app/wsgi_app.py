from flask import request
from gevent import monkey

from users_actions_app.action_app import create_action_app

monkey.patch_all()


app = create_action_app()


@app.before_request
def before_request():
    request_id = request.headers.get("X-Request-Id")
    if not request_id:
        raise RuntimeError("request id is requred")
