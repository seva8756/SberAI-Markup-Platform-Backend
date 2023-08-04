from flask import jsonify, Flask

from app import Server
from app.controllers import user_controller
from app.controllers import project_controller

controllers = [user_controller, project_controller]


def register_routes(flask: Flask):
    for c in controllers:
        flask.register_blueprint(c.module)

    @flask.errorhandler(404)
    def not_found_error(error):
        return Server.error(404, "Endpoint not found")
