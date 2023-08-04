from abc import abstractmethod
from typing import List

from app.model.project.project_model import Project


class ProjectRepository:

    @abstractmethod
    def Create(self, p: Project) -> Exception:
        pass

    @abstractmethod
    def Update(self, p: Project) -> Exception:
        pass

    @abstractmethod
    def FindAllByUserId(self, id: int) -> (List[Project], Exception):
        pass

    @abstractmethod
    def Find(self, id: int) -> (List[Project], Exception):
        pass

    @abstractmethod
    def isParticipant(self, project_id: int, user_id: int) -> (List[Project], Exception):
        pass

    @abstractmethod
    def Join(self, project_id: int, user_id: int) -> Exception:
        pass

    @abstractmethod
    def SetAnswer(self, project_id: int, task_id: int, user_id: int, answer: str, execution_time: int) -> Exception:
        pass
