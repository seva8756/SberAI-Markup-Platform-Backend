import http

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.server.server import Server
from ..decorators.validate_json import validate_json
from ..service.project_service import ProjectService

from ..controllers import errors

module = Blueprint('projects', __name__, url_prefix="/projects")


@module.route('/all', methods=['GET'])
@jwt_required()
def projects_all():
    user_id = get_jwt_identity()
    data, err = ProjectService.get_all_projects(user_id)
    if err is not None:
        return Server.error(http.HTTPStatus.INTERNAL_SERVER_ERROR, 'Error getting projects')
    return Server.respond(http.HTTPStatus.OK, data)


@module.route('/task-selection/<int:project_id>', methods=['GET'])
@jwt_required()
def projects_sampling_task(project_id: int):
    user_id = get_jwt_identity()
    data, err = ProjectService.get_actual_task_in_project(project_id, user_id)
    if err is not None:
        if err in [errors.errNoAccessToTheProject, errors.errProjectNotFound, errors.errNoTasksAvailable]:
            return Server.error(http.HTTPStatus.FORBIDDEN, err)
        return Server.error(http.HTTPStatus.INTERNAL_SERVER_ERROR, err)

    return Server.respond(http.HTTPStatus.OK, data)


@module.route('<int:project_id>/task/<int:task_id>', methods=['GET'])
@jwt_required()
def projects_get_task(project_id: int, task_id: int):
    if task_id is None:
        return Server.error(http.HTTPStatus.BAD_REQUEST, errors.errInvalidJsonData)

    user_id = get_jwt_identity()
    data, err = ProjectService.get_task_from_history_by_id(project_id, task_id, user_id)
    if err is not None:
        if err in [errors.errNoAccessToTheProject, errors.errProjectNotFound, errors.errTaskNotFound,
                   errors.errNoAccessToTask]:
            return Server.error(http.HTTPStatus.FORBIDDEN, err)
        return Server.error(http.HTTPStatus.INTERNAL_SERVER_ERROR, err)

    return Server.respond(http.HTTPStatus.OK, data)


@module.route('/task-answer', methods=['POST'])
@validate_json
@jwt_required()
def projects_answer_task():
    project_id = request.json.get('project_id')
    task_id = request.json.get('task_id')
    answer_list = request.json.get('answer')
    if project_id is None or task_id is None or answer_list is None or not isinstance(answer_list, dict):
        return Server.error(http.HTTPStatus.BAD_REQUEST, errors.errInvalidJsonData)

    user_id = get_jwt_identity()
    err = ProjectService.set_answer_for_project_task(project_id, answer_list, task_id, user_id)
    if err is not None:
        if err in [errors.errNoAccessToTheProject, errors.errProjectNotFound, errors.errAnswerOptionDoesNotExist,
                   errors.errTaskNotReservedForUser, errors.errTaskNotFound, errors.errPhotoUploadFailed]:
            return Server.error(http.HTTPStatus.FORBIDDEN, err)
        return Server.error(http.HTTPStatus.INTERNAL_SERVER_ERROR, err)

    return Server.respond(http.HTTPStatus.OK, "Answer fixed")


@module.route('/join', methods=['POST'])
@validate_json
@jwt_required()
def projects_join():
    code = request.json.get('code')
    password = request.json.get('password')
    if code is None or password is None:
        return Server.error(http.HTTPStatus.BAD_REQUEST, errors.errInvalidJsonData)

    user_id = get_jwt_identity()
    data, err = ProjectService.join_to_project(code, password, user_id)
    if err is not None:
        if err in [errors.errAlreadyInProject, errors.errProjectNotFound, errors.errWrongPassword]:
            return Server.error(http.HTTPStatus.FORBIDDEN, err)
        return Server.error(http.HTTPStatus.INTERNAL_SERVER_ERROR, err)

    return Server.respond(http.HTTPStatus.OK, data)
