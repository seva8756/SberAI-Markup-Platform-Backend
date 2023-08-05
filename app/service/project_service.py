from typing import Dict

from .. import Server
from ..controllers import errors
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
            config, err = Server.file_store().Project().get_config(project)
            if err is not None:
                print(f"Error reading the project config ({project.directory}):", err)
                continue
            projects_general_info.append(project.get_general_information())

        return projects_general_info, None

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
        project, err = Server.file_store().Project().get_config(project)
        if err is not None:
            return None, err
        project, err = Server.file_store().Project().get_csv(project)
        if err is not None:
            return None, err

        result = Server.file_store().Project().get_sampling_tasks(project, user_id)
        if len(result) == 0:
            return None, errors.errNoTasksAvailable
        selected_task = result.iloc[0]

        data = {
            "index": int(selected_task.name),
            "images": Server.file_store().Project().get_images_by_fields_name(project, selected_task,
                                                                              project.config.question_fields),
        }
        if project.config.answer_type == project.config.ANSWER_TYPE_TEXT:
            data["placeholder"] = selected_task[
                project.config.placeholder_fields] if project.config.placeholder_fields is not None else ""
        Server.file_store().Project().reserve_task_by_user_id(project, selected_task, user_id)
        return data, None

    @staticmethod
    def set_answer_for_project_task(project_id: int, answer: str, task_id: int, user_id: int) -> Exception:
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
        project, err = Server.file_store().Project().get_config(project)
        if err is not None:
            return err
        project, err = Server.file_store().Project().get_csv(project)
        if err is not None:
            return err

        if project.config.answer_type == project.config.ANSWER_TYPE_CHOICE:
            if answer not in project.config.answer_choice:
                return errors.errAnswerOptionDoesNotExist

        execution_time_seconds, err = Server.file_store().Project().set_answer_task(project, answer, task_id, user_id)
        if err is not None:
            if err == file_db_errors.ErrTaskNotReservedForUser:
                return errors.errTaskNotReservedForUser
            elif err == file_db_errors.ErrTaskNotFound:
                return errors.errTaskNotFound
            return err
        err = Server.store().Project().SetAnswer(project_id, task_id, user_id, answer,
                                                 execution_time_seconds)
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

        project, err = Server.file_store().Project().get_config(project)
        if err is not None:
            return None, err

        if project.config.password != password:
            return None, errors.errWrongPassword
        err = Server.store().Project().Join(project_id, user_id)
        if err is not None:
            return None, err

        return project.get_general_information(), None
