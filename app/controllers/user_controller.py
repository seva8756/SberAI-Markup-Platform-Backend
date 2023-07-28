import http

from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.decorators.validate_json import validate_json
from app.server.server import Server
from ..service.user_service import UserService
from ..store.errors import ErrRecordAlreadyExist, ErrRecordNotFound

module = Blueprint('users', __name__, url_prefix="/users")


def set_auth_cookie(response, data):
    expiration_delta_access = int(current_app.config["JWT_ACCESS_TOKEN_EXPIRES"].total_seconds())
    expiration_delta_refresh = int(current_app.config["JWT_REFRESH_TOKEN_EXPIRES"].total_seconds())
    response.set_cookie('refresh_token', data["refresh_token"], httponly=True, max_age=expiration_delta_refresh)
    response.set_cookie('access_token', data["access_token"], httponly=True, max_age=expiration_delta_access)


@module.route('/create', methods=['POST'])
@validate_json
def users_create():
    email = request.json.get('email')
    password = request.json.get('password')
    fist_name = request.json.get('firstName')
    last_name = request.json.get('lastName')
    if email is None or password is None or fist_name is None or last_name is None:
        return Server.error(http.HTTPStatus.BAD_REQUEST, 'Invalid JSON data')

    data, err = UserService.register(email, password, fist_name, last_name)

    if err is not None:
        if err == ErrRecordAlreadyExist:
            return Server.error(http.HTTPStatus.CONFLICT, 'Email already exists')
        return Server.error(http.HTTPStatus.UNPROCESSABLE_ENTITY, err)

    response = Server.respond(http.HTTPStatus.CREATED, data["user_data"])
    set_auth_cookie(response, data)
    return response


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

    response = Server.respond(http.HTTPStatus.OK, data["user_data"])
    set_auth_cookie(response, data)
    return response


@module.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def users_refresh():
    refresh_token = request.cookies.get('refresh_token')

    data, err = UserService.refresh(refresh_token)
    if err is not None:
        return Server.error(http.HTTPStatus.UNAUTHORIZED, err)

    response = Server.respond(http.HTTPStatus.OK, "Refresh successful")
    set_auth_cookie(response, data)
    return response


@module.route('/logout', methods=['POST'])
@jwt_required(refresh=True)
def users_logout():
    refresh_token = request.cookies.get('refresh_token')
    err = UserService.logout(refresh_token)
    if err is not None:
        return Server.error(http.HTTPStatus.UNAUTHORIZED, "Logout denied")

    response = Server.respond(http.HTTPStatus.OK, "Logout successful")
    response.delete_cookie('refresh_token')
    response.delete_cookie('access_token')
    return response


@module.route('/info/personal', methods=['GET'])
@jwt_required()
def users_get_info_personal():
    user_id = get_jwt_identity()
    data, err = UserService.get_user_info(user_id)
    if err is not None:
        if err == ErrRecordNotFound:
            return Server.error(http.HTTPStatus.NOT_FOUND, "User with this id was not found")
        return Server.error(http.HTTPStatus.BAD_REQUEST, "Get info interrupted")

    return Server.respond(http.HTTPStatus.OK, data)
