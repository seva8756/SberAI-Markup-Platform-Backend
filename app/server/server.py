import http
import json

import flask
from flask import (
    Flask,
    jsonify,
    make_response,
    current_app
)
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.store.store import Store
from app.config import Config


class Server:
    _flask: Flask
    _store: Store

    def __init__(self, store: Store, config: Config.flask):
        app = Flask(__name__)
        app.config.from_object(config)
        JWTManager(app)
        CORS(app, supports_credentials=True)  # CORS(app, resources={"*": {"origins": ""}}, supports_credentials=True)

        self.flask = app
        self.store = store

        app.config["current_server"] = self

        self._configure_router()

    def _configure_router(self):
        from app.router import router
        router.register_routes(self)

    @staticmethod
    def error(code: int, error):
        if isinstance(error, Exception):
            error = str(error)
        return Server.respond(code, {"error": error})

    @staticmethod
    def respond(code: int, data=None):
        return make_response(jsonify(data), code)

    @staticmethod
    def store() -> Store:
        return current_app.config["current_server"].store

    @staticmethod
    def flask() -> Store:
        return current_app.config["current_server"].flask
