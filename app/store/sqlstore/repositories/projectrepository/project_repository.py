from functools import reduce
from typing import List

import app.store as store
from app.model.project.project_model import Project
from app.store import errors
from app.store.errors import ErrRecordNotFound
from app.store.store import Store


class ProjectRepository(store.ProjectRepository):
    store: Store

    def __init__(self, store: Store):
        self.store = store

    def Create(self, p: Project) -> Exception:
        _, err, info = self.store.query("INSERT INTO projects (directory) VALUES (%s)",
                                        p.directory)
        if err is not None:
            return err
        p.ID = info.last_row_id

    def Update(self, p: Project) -> Exception:
        if not hasattr(p, "ID"):
            return AttributeError("Token has no ID")
        _, err, _ = self.store.query("UPDATE projects SET directory = %s WHERE ID = %s",
                                     p.directory,
                                     p.ID)
        if err is not None:
            return err

    def FindAllByUserId(self, id: int) -> (List[Project], Exception):
        res, err, _ = self.store.query(
            "SELECT project FROM projects_participants WHERE user = %s",
            id)
        if err is not None:
            return None, err
        if len(res) == 0:
            return [], None

        formatted_ids = ', '.join(str(item[0]) for item in res)
        res, err, _ = self.store.query(
            f"SELECT ID, directory, closed FROM projects WHERE id IN ({formatted_ids})")
        if err is not None:
            return None, err

        projects: List[Project] = []
        for project in res:
            p = Project()
            p.ID = project[0]
            p.directory = project[1]
            p.closed = project[2]
            projects.append(p)
        return projects, None

    def Find(self, id: int) -> (Project, Exception):
        res, err, _ = self.store.query(
            "SELECT ID, directory, closed FROM projects WHERE ID = %s AND DELETED = 0", id)
        if err is not None:
            return None, err
        if len(res) == 0:
            return None, ErrRecordNotFound

        p = Project()
        p.ID = res[0][0]
        p.directory = res[0][1]
        p.closed = res[0][2]
        return p, None

    def FindCompletedTasks(self, user_id: int, project_id: int) -> (list[int], Exception):
        res, err, _ = self.store.query(
            "SELECT task FROM completed_tasks WHERE user = %s AND project = %s",
            user_id,
            project_id)
        if err is not None:
            return None, err

        return list(map(lambda item: item[0], res)), None

    def isParticipant(self, project_id: int, user_id: int) -> (bool, Exception):
        res, err, info = self.store.query(
            "SELECT ID FROM projects_participants WHERE project = %s AND user = %s",
            project_id,
            user_id)
        if err is not None:
            return False, err

        if len(res) == 0:
            return False, None
        return True, None

    def Join(self, project_id: int, user_id: int) -> Exception:
        res, err, _ = self.store.query(
            "INSERT INTO projects_participants (project, user) VALUES (%s, %s)",
            project_id,
            user_id)
        if err is not None:
            return err

    def SetAnswer(self, project_id: int, task_id: int, user_id: int, answer: str, execution_time: int,
                  answer_extended: str = "") -> Exception:
        res, err, _ = self.store.query(
            "SELECT ID FROM completed_tasks WHERE user = %s AND project = %s AND task = %s",
            user_id,
            project_id,
            task_id)
        if err is not None:
            return err

        if len(res) > 0:
            res, err, _ = self.store.query(
                "UPDATE completed_tasks SET answer = %s, answer_extended = %s WHERE ID = %s",
                answer,
                answer_extended,
                res[0][0])
            if err is not None:
                return err
        else:
            res, err, _ = self.store.query(
                "INSERT INTO completed_tasks (user, project, task, answer, answer_extended, execution_time) VALUES (%s, %s, %s, %s, %s, %s)",
                user_id,
                project_id,
                task_id,
                answer,
                answer_extended,
                execution_time)
            if err is not None:
                return err
