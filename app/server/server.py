from flask import Flask

from app.store.store import Store
from app.config import Config


class Server:
    flask: Flask
    store: Store

    def __init__(self, store: Store, config: Config.Flask = None):
        app = Flask(__name__)
        app.config.from_object(config)

        self.flask = app
        self.store = store

        self.configure_router(app)

    def configure_router(self, app):
        @app.route('/users', methods=['POST'])
        def users():
            # print(app.store.User().create())
            return "Hello world@"

        pass
