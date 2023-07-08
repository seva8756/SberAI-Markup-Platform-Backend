from abc import abstractmethod
from app.model import User


class UserRepository:

    @abstractmethod
    def Create(self, u: User):
        pass

    @abstractmethod
    def FindByEmail(self, string: str):
        pass
