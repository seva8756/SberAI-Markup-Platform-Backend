import random
from typing import Dict

from pandas import Series

from .. import Server
from ..controllers import errors
from ..model.project.project_config_model import ComponentsPurposeTypes, ComponentsContentTypes, ProjectConfig
from ..model.project.project_model import Project
from ..store import errors as db_errors
from ..file_store import errors as file_db_errors
from ..utils import utils


class ProjectService:

    @staticmethod
    def get_all_projects(user_id: int) -> (Dict[str, str], Exception):
        projects, err = Server.store().Project().FindAllByUserId(user_id)
        if err is not None:
            return None, err

        projects_general_info = []
        for project in projects:
            err = Server.file_store().Project().load_project(project, False)
            if err is not None:
                print(f"Error reading the project config ({project.directory}):", err)
                continue

            data, err = ProjectUtils.get_project_data(project, user_id)
            if err is not None:
                return None, err
            projects_general_info.append(data)

        return projects_general_info, None

    @staticmethod
    def get_task_from_history_by_id(project_id: int, task_id: int, user_id: int) -> (Dict[str, str], Exception):
        is_participant, err = Server.store().Project().isParticipant(project_id, user_id)
        if err is not None:
            return None, err
        if not is_participant:
            return None, errors.errNoAccessToTheProject

        project, err = Server.store().Project().Find(project_id)
        if err is not None:
            if err == db_errors.ErrRecordNotFound:
                return None, errors.errProjectNotFound
            return None, err
        err = Server.file_store().Project().load_project(project)
        if err is not None:
            return None, err

        task, err = Server.file_store().Project().get_task(project, task_id)
        if err is not None:
            return None, err
        answer, err = Server.file_store().Project().get_task_answer(project, task, user_id)
        if err is not None:
            if err == file_db_errors.ErrAnswerNotFound:
                return None, errors.errNoAccessToTask
            return None, err

        data = ProjectUtils.get_task_data(project, task)
        return {"answer": answer, **data}, None

    @staticmethod
    def get_actual_task_in_project(project_id: int, user_id: int) -> (Dict[str, str], Exception):
        is_participant, err = Server.store().Project().isParticipant(project_id, user_id)
        if err is not None:
            return None, err
        if not is_participant:
            return None, errors.errNoAccessToTheProject

        project, err = Server.store().Project().Find(project_id)
        if err is not None:
            if err == db_errors.ErrRecordNotFound:
                return None, errors.errProjectNotFound
            return None, err
        err = Server.file_store().Project().load_project(project)
        if err is not None:
            return None, err

        result = Server.file_store().Project().get_sampling_tasks(project, user_id)
        if len(result) == 0:
            return None, errors.errNoTasksAvailable
        task_index = random.randint(0, len(result) - 1) if project.config.random_sampling else 0
        selected_task = result.iloc[task_index]

        data = ProjectUtils.get_task_data(project, selected_task)
        Server.file_store().Project().reserve_task(project, selected_task, user_id)
        return data, None

    @staticmethod
    def set_answer_for_project_task(project_id: int, answer_list: dict[str, str], task_id: int,
                                    user_id: int) -> Exception:
        is_participant, err = Server.store().Project().isParticipant(project_id, user_id)
        if err is not None:
            return err
        if not is_participant:
            return errors.errNoAccessToTheProject

        project, err = Server.store().Project().Find(project_id)
        if err is not None:
            if err == db_errors.ErrRecordNotFound:
                return errors.errProjectNotFound
            return err
        err = Server.file_store().Project().load_project(project)
        if err is not None:
            return err

        answer_list, err = ProjectUtils.before_answer(project, answer_list)
        if err is not None:
            return err

        execution_time_seconds, err = Server.file_store().Project().set_answer_task(project, answer_list,
                                                                                    task_id, user_id)
        if err is not None:
            if err == file_db_errors.ErrTaskNotReservedForUser:
                return errors.errTaskNotReservedForUser
            elif err == file_db_errors.ErrTaskNotFound:
                return errors.errTaskNotFound
            elif err == file_db_errors.ErrPhotoUploadFailed:
                return errors.errPhotoUploadFailed
            return err
        err = Server.store().Project().SetAnswer(project_id, task_id, user_id, answer_list, execution_time_seconds)
        if err is not None:
            return err

    @staticmethod
    def join_to_project(code: str, password: str, user_id: int) -> (dict[str, str], Exception):
        project_id = utils.ProjectCode.decode_id(code)

        project, err = Server.store().Project().Find(project_id)
        if err is not None:
            if err == db_errors.ErrRecordNotFound:
                return None, errors.errProjectNotFound
            return None, err

        is_participant, err = Server.store().Project().isParticipant(project_id, user_id)
        if err is not None:
            return None, err
        if is_participant:
            return None, errors.errAlreadyInProject

        err = Server.file_store().Project().load_project(project, False)
        if err is not None:
            return None, err

        if project.config.password != password:
            return None, errors.errWrongPassword
        err = Server.store().Project().Join(project_id, user_id)
        if err is not None:
            return None, err

        data, err = ProjectUtils.get_project_data(project, user_id)
        if err is not None:
            return None, err
        return data, None


class ProjectUtils:

    @staticmethod
    def get_task_data(project: Project, task: Series) -> dict[str, str]:
        data = {
            "index": int(task.name),
            "question": Server.file_store().Project().get_task_question(project, task),
            "components": {}
        }
        for name in project.config.components:
            result = {}

            comp = project.config.components[name]
            if ComponentsPurposeTypes.is_purpose_equal(comp,
                                                       ComponentsPurposeTypes.PURPOSE_CONTENT):  # info block in task
                if ComponentsContentTypes.is_type_equal(comp, ComponentsContentTypes.CONTENT_IMAGES):
                    result["images"] = Server.file_store().Project().get_task_images(project, comp["content_fields"],
                                                                                     task)
            elif ComponentsPurposeTypes.is_purpose_equal(comp,
                                                         ComponentsPurposeTypes.PURPOSE_ANSWER):  # answer block in task
                if ComponentsContentTypes.is_type_equal(comp, ComponentsContentTypes.CONTENT_INPUT):
                    result["placeholder"] = Server.file_store().Project().get_task_placeholder(
                        comp["placeholder_field"], task)
            if result:
                data["components"][name] = result
        return data

    @staticmethod
    def get_project_data(project: Project, user_id: int = None) -> (dict[str, str], Exception):
        data = {
            **project.get_general_information(),
            "completed_tasks": []
        }
        if user_id is not None:
            tasks, err = Server.store().Project().FindCompletedTasks(user_id, project.ID)
            if err is not None:
                return None, err
            data["completed_tasks"] = tasks
        return data, None

    @staticmethod
    def before_answer(project: Project, answer: dict[str, str]) -> (str, Exception):
        cleaning_unnecessary = {}
        for name in project.config.components:
            component = project.config.components[name]
            if name in answer:
                if ComponentsPurposeTypes.is_purpose_equal(component, ComponentsPurposeTypes.PURPOSE_ANSWER):
                    cleaning_unnecessary[name] = answer[name]
        answer = cleaning_unnecessary

        for name in project.config.components:
            component = project.config.components[name]
            if ProjectConfig.is_component_require(component):
                if name not in answer or not answer[name].strip():
                    return None, errors.errMissingRequiredComponent

        for name in answer:
            ans = answer[name]
            component = project.config.components[name]
            if ComponentsPurposeTypes.is_purpose_equal(component, ComponentsPurposeTypes.PURPOSE_ANSWER):
                if ComponentsContentTypes.is_type_equal(component, ComponentsContentTypes.CONTENT_CHOICE):
                    if ans not in component["options"]:
                        return None, errors.errAnswerOptionDoesNotExist

        return answer, None
