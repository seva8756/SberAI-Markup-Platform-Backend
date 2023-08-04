from flask import (
    Flask,
    jsonify,
    make_response,
    current_app, Response
)
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.file_store import FileStore
from app.store.store import Store
from app.config import Config


class Server:
    flask: Flask
    store: Store
    file_store_: FileStore = FileStore()

    def __init__(self, store: Store, config: Config.flask):
        app = Flask(__name__)
        app.config.from_object(config)
        JWTManager(app)
        CORS(app, supports_credentials=True)  # CORS(app, resources={"*": {"origins": ""}}, supports_credentials=True)

        self.flask = app
        self.store = store

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
        return current_app.config["current_server"].file_store_

    @staticmethod
    def flask() -> Store:
        return current_app.config["current_server"].flask
