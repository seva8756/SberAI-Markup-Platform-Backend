from abc import abstractmethod

from app.store.repositories.project_repository import ProjectRepository
from app.store.repositories.token_repository import TokenRepository
from app.store.repositories.user_repository import UserRepository


class Store:

    @abstractmethod
    def query(self, query: str, *args, one=False) -> (any, Exception):
        pass

    @abstractmethod
    def User(self) -> UserRepository:
        pass

    @abstractmethod
    def Token(self) -> TokenRepository:
        pass

    @abstractmethod
    def Project(self) -> ProjectRepository:
        pass
