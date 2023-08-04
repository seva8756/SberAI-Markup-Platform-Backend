import http
from functools import wraps

from app.controllers import errors
from app.server.server import Server

from flask import (
    request
)


def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kw):
        try:
            if not isinstance(request.get_json(), dict):
                raise
        except Exception:
            return Server.error(http.HTTPStatus.BAD_REQUEST, errors.errInvalidJsonFormat)
        return f(*args, **kw)

    return wrapper
