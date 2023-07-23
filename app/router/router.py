from app import Server
from app.controllers import user_controller

controllers = [user_controller]


def register_blueprints(server: Server):
    for c in controllers:
        server.flask.register_blueprint(c.module)
