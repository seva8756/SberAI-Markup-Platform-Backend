import json
import os
import time
from datetime import timedelta
from typing import List, Callable

import pandas as pd
from pandas import DataFrame

from app.file_store import errors
from app.model.project.project_config_model import ProjectConfig
from app.model.project.project_model import Project
from app.utils import utils


class ProjectFileRepository:
    projects_data = utils.get_project_root() + "/data/projects/"
    projects_config = projects_data + "%s/config.json"
    projects_tasks = projects_data + "%s/tasks.csv"
    projects_content = projects_data + "%s/content/"

    task_reserved_seconds = timedelta(minutes=30)

    user_prefix = "user_"

    def check_reserved(self):
        projects_dir = os.listdir(self.projects_data)
        for dir in projects_dir:
            p = Project()
            p.directory = dir
            p, err = self.get_csv(p)
            if err is not None:
                continue

            if "reserved" not in p.csv.columns:
                self._update_reserved(p, row=None, obj={})
            else:
                for index, row in p.csv.iterrows():
                    users_reserved = self._get_reserved(row)
                    users_reserved_formatted = users_reserved.copy()
                    for id in users_reserved:
                        timestamp = users_reserved[id]
                        time_over = (int(time.time()) - timestamp) > self.task_reserved_seconds.total_seconds()
                        if time_over:
                            del users_reserved_formatted[id]
                            continue
                    self._update_reserved(p, row, users_reserved_formatted)
            self.save_csv(p)

    def get_config(self, p: Project) -> (Project, Exception):
        try:
            with open(self.projects_config % p.directory, 'r',
                      encoding='utf-8') as json_file:
                data = json.load(json_file)
                p.config = ProjectConfig(**data)
        except Exception as err:
            return None, err
        return p, None

    def get_csv(self, p: Project) -> (Project, Exception):
        try:
            df = pd.read_csv(self.projects_tasks % p.directory, na_filter=False)
            p.csv = df
        except Exception as err:
            return None, err
        return p, None

    def get_sampling_tasks(self, project: Project, user_id: int) -> DataFrame:
        user_prefix_id = f"{self.user_prefix}{user_id}"

        def is_reserved(row):
            return str(user_id) in self._get_reserved(row)

        # is already reserved for this user_id
        reserved_tasks = project.csv.loc[project.csv.apply(is_reserved, axis=1)]
        if len(reserved_tasks) > 0:
            return reserved_tasks

        def is_row_empty(row: DataFrame, col):
            return str(row[col]).strip() == ""

        def count_completed(row):
            reserved = self.count_reserved(row, user_id)
            already_completed = sum(
                not is_row_empty(row, col) for col in project.csv.columns if col.startswith(self.user_prefix))
            return already_completed + reserved

        check_callbacks: List[Callable[[DataFrame], bool]] = []
        # user_not_perform
        if user_prefix_id in project.csv.columns:
            check_callbacks.append(lambda row: is_row_empty(row, user_prefix_id))

        # not_max_resolves
        check_callbacks.append(lambda row: count_completed(row) < project.config.repeated_tasks)

        def check(row):
            result_condition = check_callbacks[0](row)
            for callback in check_callbacks[1:]:
                result_condition = result_condition & callback(row)
            return result_condition

        return project.csv.loc[project.csv.apply(check, axis=1)]

    def get_images_by_fields_name(self, p: Project, row: DataFrame, fields: List[str]) -> List[str]:
        images = []
        for content_field in fields:
            image = utils.get_image_in_base64(
                f"{self.projects_content % p.directory}/{row[content_field]}")
            images.append(image)
        return images

    def count_reserved(self, row, user_id: int) -> int:
        users_reserved = self._get_reserved(row)
        if user_id in users_reserved:
            return len(users_reserved) - 1
        else:
            return len(users_reserved)

    def reserve_task_by_user_id(self, p: Project, row, user_id: int) -> int:
        try:
            reserved = self._get_reserved(row)
            reserved[str(user_id)] = int(time.time())
            self._update_reserved(p, row, reserved)
            self.save_csv(p)
        except Exception as err:
            print("Reserve user_id failed:", err)

    # returning second from start of reservation to response
    def remove_reserve_task_by_user_id(self, p: Project, row, user_id: int) -> (int, Exception):
        try:
            user_id_str = str(user_id)
            reserved = self._get_reserved(row)
            if user_id_str not in reserved:
                return None, errors.ErrTaskNotReservedForUser

            execution_time_seconds = int(time.time()) - reserved[user_id_str]
            del reserved[user_id_str]
            self._update_reserved(p, row, reserved)
            self.save_csv(p)
            return execution_time_seconds, None
        except Exception as err:
            print("Remove reserve user_id failed:", err)

    def set_answer_task(self, p: Project, answer: str, task_id: int, user_id: int) -> (int, Exception):
        try:
            execution_time_seconds, err = self.remove_reserve_task_by_user_id(p, p.csv.iloc[task_id], user_id)
            if err is not None:
                return None, err

            user_prefix_id = f"{self.user_prefix}{user_id}"
            if user_prefix_id not in p.csv.columns:
                p.csv[user_prefix_id] = ""
            p.csv.at[task_id, user_prefix_id] = answer

            self.save_csv(p)
            return execution_time_seconds, None
        except IndexError:
            return None, errors.ErrTaskNotFound
        except Exception as err:
            print("Set answer user_id failed:", err)
            return None, err

    def _update_reserved(self, p: Project, row, obj: dict[str, int]):
        try:
            if row is not None:
                p.csv.at[row.name, "reserved"] = json.dumps(obj)
            else:
                p.csv["reserved"] = json.dumps(obj)
        except Exception as err:
            print("Update reserved json failed:", err)

    def _get_reserved(self, row) -> dict[str, int]:
        try:
            return json.loads(row["reserved"])
        except Exception as err:
            print("Load reserved json failed:", err)
            return {}

    def save_csv(self, project: Project):
        try:
            project.csv.to_csv(self.projects_tasks % project.directory, index=False)
        except Exception as err:
            print("Update reserved json failed: ", err)
