import http

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.decorators.validate_json import validate_json
from app.server.server import Server
from ..service.user_service import UserService
from ..store.errors import ErrRecordAlreadyExist

module = Blueprint('users', __name__, url_prefix="/users")


@module.route('/create', methods=['POST'])
@validate_json
def users_create():
    email = request.json.get('email')
    password = request.json.get('password')
    if email is None or password is None:
        return Server.error(http.HTTPStatus.BAD_REQUEST, 'Invalid JSON data')

    data, err = UserService.register(email, password)

    if err is not None:
        if err == ErrRecordAlreadyExist:
            return Server.error(http.HTTPStatus.CONFLICT, 'Email already exists')
        return Server.error(http.HTTPStatus.UNPROCESSABLE_ENTITY, err)

    return Server.respond(http.HTTPStatus.CREATED, data)


@module.route('/login', methods=['POST'])
@validate_json
def users_sessions():
    email = request.json.get('email')
    password = request.json.get('password')
    if email is None or password is None:
        return Server.error(http.HTTPStatus.BAD_REQUEST, 'Invalid JSON data')

    data, err = UserService.login(email, password)
    if err is not None:
        return Server.error(http.HTTPStatus.UNAUTHORIZED, err)
    return Server.respond(http.HTTPStatus.OK, data)


@module.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def users_refresh():
    refresh_token = request.headers.get('Authorization').split(' ')[1]

    data, err = UserService.refresh(refresh_token)
    if err is not None:
        return Server.error(http.HTTPStatus.UNAUTHORIZED, err)

    return Server.respond(http.HTTPStatus.OK, data)


@module.route('/logout', methods=['POST'])
@jwt_required(refresh=True)
def users_logout():
    refresh_token = request.headers.get('Authorization').split(' ')[1]
    err = UserService.logout(refresh_token)
    if err is not None:
        return Server.error(http.HTTPStatus.UNAUTHORIZED, "Logout denied")

    return Server.respond(http.HTTPStatus.OK, "Logout success")
