import random
from typing import Dict

from pandas import Series

from .. import Server
from ..controllers import errors
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
            config, err = Server.file_store().Project().get_config(project)
            if err is not None:
                print(f"Error reading the project config ({project.directory}):", err)
                continue

            tasks, err = Server.store().Project().FindCompletedTasks(user_id, project.ID)
            if err is not None:
                return None, err
            projects_general_info.append({"completed_tasks": tasks, **project.get_general_information()})

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
        project, err = Server.file_store().Project().get_config(project)
        if err is not None:
            return None, err
        project, err = Server.file_store().Project().get_csv(project)
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
        project, err = Server.file_store().Project().get_config(project)
        if err is not None:
            return None, err
        project, err = Server.file_store().Project().get_csv(project)
        if err is not None:
            return None, err

        result = Server.file_store().Project().get_sampling_tasks(project, user_id)
        if len(result) == 0:
            return None, errors.errNoTasksAvailable
        random_number = random.randint(0, len(result) - 1)
        selected_task = result.iloc[random_number]

        data = ProjectUtils.get_task_data(project, selected_task)
        Server.file_store().Project().reserve_task_by_user_id(project, selected_task, user_id)
        return data, None

    @staticmethod
    def set_answer_for_project_task(project_id: int, answer: str, answer_extended: str, task_id: int,
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
        project, err = Server.file_store().Project().get_config(project)
        if err is not None:
            return err
        project, err = Server.file_store().Project().get_csv(project)
        if err is not None:
            return err

        answer, err = ProjectUtils.before_answer(project, answer)
        if err is not None:
            return err

        execution_time_seconds, err = Server.file_store().Project().set_answer_task(project, answer, answer_extended,
                                                                                    task_id, user_id)
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


class ProjectUtils:

    @staticmethod
    def get_task_data(project: Project, task: Series) -> dict[str, str]:
        data = {
            "index": int(task.name),
        }
        if project.config.answer_type in [project.config.ANSWER_TYPE_TEXT]:
            data["placeholder"] = task[
                project.config.placeholder_fields] if project.config.placeholder_fields is not None else ""
        if project.config.answer_type in [project.config.ANSWER_TYPE_TEXT, project.config.ANSWER_TYPE_CHOICE]:
            data["images"] = Server.file_store().Project().get_images_by_fields_name(project, task,
                                                                                     project.config.question_fields),
        return data

    @staticmethod
    def before_answer(project: Project, answer: str) -> (str, Exception):
        if project.config.answer_type in [project.config.ANSWER_TYPE_CHOICE]:
            if answer not in project.config.answer_choice:
                return None, errors.errAnswerOptionDoesNotExist

        return answer, None
