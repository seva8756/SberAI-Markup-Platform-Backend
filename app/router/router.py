from flask import jsonify

from app import Server
from app.controllers import user_controller

controllers = [user_controller]


def register_routes(server: Server):
    flask = server.flask
    for c in controllers:
        flask.register_blueprint(c.module)

    @flask.errorhandler(404)
    def not_found_error(error):
        return Server.error(404, "Endpoint not found")
