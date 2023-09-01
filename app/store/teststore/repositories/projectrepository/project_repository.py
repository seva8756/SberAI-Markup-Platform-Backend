from functools import reduce
from typing import List, Dict

import app.store as store
from app.model.project.project_model import Project
from app.store import errors
from app.store.errors import ErrRecordNotFound
from app.store.store import Store

Projects = Dict[int, Project]
ProjectsParticipants = Dict[int, List[int]]
CompletedTasks = List[Dict[str, str]]


class ProjectRepository(store.ProjectRepository):
    store: Store
    projects: Projects
    projects_participants: ProjectsParticipants
    completed_tasks: CompletedTasks

    def __init__(self, store: Store, projects: Projects, projects_participants: ProjectsParticipants,
                 completed_tasks: CompletedTasks):
        self.store = store
        self.projects = projects
        self.projects_participants = projects_participants
        self.completed_tasks = completed_tasks

    def Create(self, p: Project) -> Exception:
        p.ID = len(self.projects) + 1
        self.projects[p.ID] = p

    def Update(self, p: Project) -> Exception:
        if not hasattr(p, "ID"):
            return AttributeError("Token has no ID")
        self.projects[p.ID].directory = p.directory

    def FindAllByUserId(self, id: int) -> (List[Project], Exception):
        projects: List[Project] = []
        for prj in self.projects_participants:
            for item in self.projects_participants[prj]:
                if item == id:
                    projects.append(self.projects[prj]), None

        if len(projects) == 0:
            return [], None
        return projects, None

    def Find(self, id: int) -> (Project, Exception):
        for prj in self.projects:
            if prj == id:
                return self.projects[prj], None
        return None, ErrRecordNotFound

    def FindCompletedTasks(self, user_id: int, project_id: int) -> (list[int], Exception):
        tasks = []
        for index, value in enumerate(self.completed_tasks):
            if value["user"] == user_id and value["project"] == project_id:
                tasks.append(value)

        return tasks, None

    def FindUserCompletedTasks(self, user_id: int) -> (list[int], Exception):
        tasks = []
        for index, value in enumerate(self.completed_tasks):
            if value["user"] == user_id:
                tasks.append(value)

        return tasks, None

    def isParticipant(self, project_id: int, user_id: int) -> (bool, Exception):
        if project_id in self.projects_participants:
            for item in self.projects_participants[project_id]:
                if item == user_id:
                    return True, None

        return False, None

    def Join(self, project_id: int, user_id: int) -> Exception:
        if project_id not in self.projects_participants:
            self.projects_participants[project_id] = []
        self.projects_participants[project_id].append(user_id)

    def SetAnswer(self, project_id: int, task_id: int, user_id: int, answer: str, execution_time: int) -> Exception:
        already_exist_index = None
        for index, value in enumerate(self.completed_tasks):
            if value["user"] == user_id and value["task"] == task_id and value["project"] == project_id:
                already_exist_index = index

        if already_exist_index is not None:
            self.completed_tasks[already_exist_index]["answer"] = answer
        else:
            self.completed_tasks.append({
                'user': user_id,
                'project': project_id,
                'task': task_id,
                'answer': answer,
                'execution_time': execution_time
            })
