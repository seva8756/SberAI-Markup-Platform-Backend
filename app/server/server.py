from flask import (
    Flask,
    jsonify,
    make_response,
    current_app, Response
)
from flask_cors import CORS
from flask_jwt_extended import JWTManager

import logging
from app.controllers import errors
from app.errors import ServerException
from app.file_store import FileStore
from app.store.store import Store
from app.config import Config


class Server:
    flask: Flask
    store: Store
    logger_instance: logging.Logger
    file_store_instance: FileStore = FileStore()

    def __init__(self, store: Store, config: Config.flask, logger: logging.Logger = logging.getLogger()):
        app = Flask(__name__)
        app.config.from_object(config)
        JWTManager(app)
        CORS(app, supports_credentials=True)  # CORS(app, resources={"*": {"origins": ""}}, supports_credentials=True)

        self.flask = app
        self.store = store
        self.logger_instance = logger

        app.config["current_server"] = self

        self._configure_router()
        self._configure_interval()

    def _configure_router(self):
        from app.router import router
        router.register_routes(self.flask)

    def _configure_interval(self):
        from app.interval import interval
        interval.register_interval(self)

    @staticmethod
    def error(code: int, error) -> Response:
        if not isinstance(error, ServerException):
            Server.logger().error(error)
            error = errors.errProcessing
            # Server.logger.warning("Error is not instance of ServerException. Use ServerException")
        if isinstance(error, Exception):
            error = str(error)
        return Server.respond(code, {"error": error})

    @staticmethod
    def respond(code: int, data=None) -> Response:
        return make_response(jsonify(data), code)

    @staticmethod
    def store() -> Store:
        return current_app.config["current_server"].store

    @staticmethod
    def file_store() -> FileStore:
        return current_app.config["current_server"].file_store_instance

    @staticmethod
    def flask() -> Store:
        return current_app.config["current_server"].flask

    @staticmethod
    def logger() -> logging.Logger:
        return current_app.config["current_server"].logger_instance
