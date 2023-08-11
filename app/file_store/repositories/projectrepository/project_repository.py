import json
import os
import time
from datetime import timedelta
from typing import List, Callable

import pandas as pd
from pandas import DataFrame, Series

from app.file_store import errors
from app.model.project.project_config_model import ProjectConfig
from app.model.project.project_model import Project
from app.utils import utils


class ProjectConfigManager:
    def __init__(self, projects_data):
        self.projects_data = projects_data

    def get_config_path(self, directory):
        return os.path.join(self.projects_data, directory, "config.json")

    def load_config(self, p: Project) -> (ProjectConfig, Exception):
        config_path = self.get_config_path(p.directory)
        try:
            with open(config_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                return ProjectConfig(**data), None
        except Exception as err:
            return None, err


class CsvFileManager:
    def __init__(self, projects_data):
        self.projects_data = projects_data

    def get_tasks_path(self, directory):
        return os.path.join(self.projects_data, directory, "tasks.csv")

    def load_tasks(self, p: Project) -> (DataFrame, Exception):
        tasks_path = self.get_tasks_path(p.directory)
        try:
            return pd.read_csv(tasks_path, na_filter=False), None
        except Exception as err:
            return None, err

    def save_csv(self, p: Project):
        tasks_path = self.get_tasks_path(p.directory)
        try:
            p.csv.to_csv(tasks_path, index=False)
        except Exception as err:
            print("Update reserved json failed: ", err)


class TaskReservationManager:
    def __init__(self, projects_data, task_reserved_seconds):
        self.projects_data = projects_data
        self.task_reserved_seconds = task_reserved_seconds

    def count_reserved(self, row, user_id: int) -> int:
        users_reserved = self.get_reserved(row)
        if user_id in users_reserved:
            return len(users_reserved) - 1
        else:
            return len(users_reserved)

    def reserve_task_by_user_id(self, p: Project, row, user_id: int):
        try:
            reserved = self.get_reserved(row)
            reserved[str(user_id)] = int(time.time())
            self.update_reserved(p, row, reserved)
        except Exception as err:
            print("Reserve user_id failed:", err)

    # returning second from start of reservation to response
    def remove_reserve_task_by_user_id(self, p: Project, row, user_id: int) -> (int, Exception):
        try:
            user_id_str = str(user_id)
            reserved = self.get_reserved(row)
            if user_id_str not in reserved:
                return None, errors.ErrTaskNotReservedForUser

            execution_time_seconds = int(time.time()) - reserved[user_id_str]
            del reserved[user_id_str]
            self.update_reserved(p, row, reserved)
            return execution_time_seconds, None
        except Exception as err:
            print("Remove reserve user_id failed:", err)

    def update_reserved(self, p: Project, row, obj: dict[str, int]):
        try:
            if row is not None:
                p.csv.at[row.name, "reserved"] = json.dumps(obj)
            else:
                p.csv["reserved"] = json.dumps(obj)
        except Exception as err:
            print("Update reserved json failed:", err)

    def get_reserved(self, row) -> dict[str, int]:
        try:
            return json.loads(row["reserved"])
        except Exception as err:
            print("Load reserved json failed:", err)
            return {}

    def check_reserved(self, p: Project):
        if "reserved" not in p.csv.columns:
            self.update_reserved(p, row=None, obj={})
        else:
            for index, row in p.csv.iterrows():
                users_reserved = self.get_reserved(row)
                users_reserved_formatted = users_reserved.copy()
                for id in users_reserved:
                    timestamp = users_reserved[id]
                    time_over = (int(time.time()) - timestamp) > self.task_reserved_seconds.total_seconds()
                    if time_over:
                        del users_reserved_formatted[id]
                        continue
                self.update_reserved(p, row, users_reserved_formatted)


class TaskManager:
    def __init__(self, projects_data):
        self.projects_data = projects_data

    def get_answer_image_path(self, directory: str, path: str):
        return os.path.join(self.projects_data, directory, "uploaded_content", path)

    def get_task_image_path(self, directory: str, path: str):
        return os.path.join(self.projects_data, directory, "content", path)

    def get_task(self, p: Project, task_id: int) -> (Series, Exception):
        try:
            return p.csv.iloc[task_id], None
        except IndexError:
            return None, errors.ErrTaskNotFound

    def get_task_answer(self, p: Project, row: Series, answer_column: str) -> (Series, Exception):
        try:
            answer = str(row[answer_column])
            if answer.strip() == "":
                raise KeyError()

            if p.config.answer_type in [p.config.ANSWER_TYPE_IMAGE]:
                image, err = utils.get_image_in_base64(self.get_answer_image_path(p.directory, answer))
                if err is not None:
                    return None, err
                answer = image

            return answer, None
        except KeyError:
            return None, errors.ErrAnswerNotFound

    def get_images_by_fields_name(self, p: Project, row: Series, fields: List[str]) -> List[str]:
        images = []
        for content_field in fields:
            if content_field not in row.index:
                print("Error the field is not contained in the project")
                continue
            image, err = utils.get_image_in_base64(self.get_task_image_path(p.directory, row[content_field]))
            if err is not None:
                print("Error get images by fields name:", err)
                continue
            images.append(image)
        return images


class TagManager:
    def __init__(self):
        self.user_prefix = "user_"

    def get_answer_tag(self, user_id: int):
        return f"{self.user_prefix}{user_id}"

    def get_uploaded_image_name(self, task_id: int, user_id: int):
        return f"task-{task_id}_user-{user_id}.jpg"


class ProjectFileRepository:
    def __init__(self):
        self.projects_data = utils.get_project_root() + "/data/projects/"
        self.config_manager = ProjectConfigManager(self.projects_data)
        self.csv_manager = CsvFileManager(self.projects_data)
        self.task_manager = TaskManager(self.projects_data)
        self.reservation_manager = TaskReservationManager(self.projects_data, timedelta(minutes=30))
        self.tag_manager = TagManager()

    def load_project(self, p: Project, load_tasks: bool = True) -> Exception:
        config, err = self.config_manager.load_config(p)
        if err is not None:
            return err
        p.config = config
        if load_tasks:
            tasks, err = self.csv_manager.load_tasks(p)
            if err is not None:
                return err
            p.csv = tasks

    def get_task(self, p: Project, task_id: int) -> (Series, Exception):
        return self.task_manager.get_task(p, task_id)

    def get_task_answer(self, p: Project, task: Series, user_id: int) -> (Series, Exception):
        user_prefix_id = self.tag_manager.get_answer_tag(user_id)
        return self.task_manager.get_task_answer(p, task, user_prefix_id)

    def get_sampling_tasks(self, project: Project, user_id: int) -> DataFrame:
        user_prefix_id = self.tag_manager.get_answer_tag(user_id)

        def is_reserved(row):
            return str(user_id) in self.reservation_manager.get_reserved(row)

        # is already reserved for this user_id
        reserved_tasks = project.csv.loc[project.csv.apply(is_reserved, axis=1)]
        if len(reserved_tasks) > 0:
            return reserved_tasks

        def is_answer_empty(row: Series, _user_id):
            _, err = self.get_task_answer(project, row, _user_id)
            if err is not None:
                return True
            else:
                return False

        def count_completed(row):
            reserved = self.reservation_manager.count_reserved(row, user_id)
            already_completed = sum(
                not is_answer_empty(row, col.removeprefix(self.tag_manager.user_prefix)) for col in project.csv.columns
                if col.startswith(self.tag_manager.user_prefix))
            return already_completed + reserved

        check_callbacks: List[Callable[[DataFrame], bool]] = []
        # user_not_perform
        if user_prefix_id in project.csv.columns:
            check_callbacks.append(lambda row: is_answer_empty(row, user_id))

        # not_max_resolves
        check_callbacks.append(lambda row: count_completed(row) < project.config.repeated_tasks)

        def check(row):
            result_condition = check_callbacks[0](row)
            for callback in check_callbacks[1:]:
                result_condition = result_condition & callback(row)
            return result_condition

        return project.csv.loc[project.csv.apply(check, axis=1)]

    def reserve_task(self, p: Project, task: Series, user_id: int):
        self.reservation_manager.reserve_task_by_user_id(p, task, user_id)
        self.csv_manager.save_csv(p)

    def remove_reserve_task(self, p: Project, task: Series, user_id: int) -> (int, Exception):
        execution_time_seconds, err = self.reservation_manager.remove_reserve_task_by_user_id(p, task, user_id)
        if err is not None:
            return None, err
        self.csv_manager.save_csv(p)
        return execution_time_seconds, None

    def set_answer_task(self, p: Project, answer: str, answer_extended: str, task_id: int, user_id: int) -> (
            int, Exception):
        try:
            execution_time_seconds = 0
            user_prefix_id = self.tag_manager.get_answer_tag(user_id)

            if user_prefix_id not in p.csv.columns or p.csv.at[task_id, user_prefix_id] == "":
                execution_time_seconds, err = self.remove_reserve_task(p, p.csv.iloc[task_id], user_id)
                if err is not None:
                    return None, err

            if p.config.answer_type in [p.config.ANSWER_TYPE_IMAGE]:
                image_name = self.tag_manager.get_uploaded_image_name(task_id, user_id)
                err = utils.save_base64_to_file(answer,
                                                self.task_manager.get_answer_image_path(p.directory, image_name))
                if err is not None:
                    return None, err
                answer = image_name  # we save in csv not base64, but the path to the image

            if user_prefix_id not in p.csv.columns:
                p.csv[user_prefix_id] = ""
            p.csv.at[task_id, user_prefix_id] = answer

            self.csv_manager.save_csv(p)
            return execution_time_seconds, None
        except IndexError:
            return None, errors.ErrTaskNotFound
        except Exception as err:
            print("Set answer user_id failed:", err)
            return None, err

    def get_task_images(self, p: Project, task: Series) -> list[str]:
        return self.task_manager.get_images_by_fields_name(p, task, p.config.question_fields)

    def check_reserved(self):
        projects_dir = os.listdir(self.projects_data)
        for dir in projects_dir:
            p = Project()
            p.directory = dir
            err = self.load_project(p)
            if err is not None:
                continue
            self.reservation_manager.check_reserved(p)
            self.csv_manager.save_csv(p)
