import http

from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.decorators.validate_json import validate_json
from app.server.server import Server
from . import errors
from ..service.user_service import UserService

module = Blueprint('users', __name__, url_prefix="/users")


def set_auth_cookie(response, data):
    expiration_delta_access = int(current_app.config["JWT_ACCESS_TOKEN_EXPIRES"].total_seconds())
    expiration_delta_refresh = int(current_app.config["JWT_REFRESH_TOKEN_EXPIRES"].total_seconds())
    response.set_cookie('refresh_token', data["refresh_token"], httponly=True,
                        max_age=expiration_delta_refresh)
    response.set_cookie('access_token', data["access_token"], httponly=True,
                        max_age=expiration_delta_access)


def delete_auth_cookie(response):
    response.delete_cookie('refresh_token', httponly=True)
    response.delete_cookie('access_token', httponly=True)


@module.route('/create', methods=['POST'])
@validate_json
def users_create():
    email = request.json.get('email')
    password = request.json.get('password')
    fist_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    if email is None or password is None or fist_name is None or last_name is None:
        return Server.error(http.HTTPStatus.BAD_REQUEST, errors.errInvalidJsonData)

    client_ip = request.headers.get('X-Real-IP') or request.remote_addr
    data, err = UserService.register(email, password, fist_name, last_name, client_ip)
    if err is not None:
        if err in [errors.errUserAlreadyRegistered]:
            return Server.error(http.HTTPStatus.CONFLICT, err)
        if err in [errors.errUserNotPassValidation]:
            return Server.error(http.HTTPStatus.UNPROCESSABLE_ENTITY, err)
        return Server.error(http.HTTPStatus.INTERNAL_SERVER_ERROR, err)

    response = Server.respond(http.HTTPStatus.CREATED, data["user_data"])
    set_auth_cookie(response, data)
    return response


@module.route('/login', methods=['POST'])
@validate_json
def users_sessions():
    email = request.json.get('email')
    password = request.json.get('password')
    if email is None or password is None:
        return Server.error(http.HTTPStatus.BAD_REQUEST, errors.errInvalidJsonData)

    data, err = UserService.login(email, password)
    if err is not None:
        if err in [errors.errIncorrectEmailOrPassword]:
            return Server.error(http.HTTPStatus.UNAUTHORIZED, err)
        return Server.error(http.HTTPStatus.INTERNAL_SERVER_ERROR, err)

    response = Server.respond(http.HTTPStatus.OK, data["user_data"])
    set_auth_cookie(response, data)
    return response


@module.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def users_refresh():
    refresh_token = request.cookies.get('refresh_token')

    data, err = UserService.refresh(refresh_token)
    if err is not None:
        if err in [errors.errSessionNotFound]:
            return Server.error(http.HTTPStatus.UNAUTHORIZED, err)
        return Server.error(http.HTTPStatus.INTERNAL_SERVER_ERROR, err)

    response = Server.respond(http.HTTPStatus.OK, "Refresh successful")
    set_auth_cookie(response, data)
    return response


@module.route('/logout', methods=['POST'])
@jwt_required(refresh=True)
def users_logout():
    refresh_token = request.cookies.get('refresh_token')
    err = UserService.logout(refresh_token)
    if err is not None:
        if err in [errors.errSessionNotFound]:
            return Server.error(http.HTTPStatus.NOT_FOUND, err)
        return Server.error(http.HTTPStatus.INTERNAL_SERVER_ERROR, err)

    response = Server.respond(http.HTTPStatus.OK, "Logout successful")
    delete_auth_cookie(response)
    return response


@module.route('/info/personal', methods=['GET'])
@jwt_required()
def users_get_info_personal():
    user_id = get_jwt_identity()
    data, err = UserService.get_user_info(user_id)
    if err is not None:
        if err in [errors.errUserNotFound]:
            return Server.error(http.HTTPStatus.NOT_FOUND, err)
        return Server.error(http.HTTPStatus.INTERNAL_SERVER_ERROR, err)

    return Server.respond(http.HTTPStatus.OK, data)
