from abc import abstractmethod
from app.model import User


class UserRepository:

    @abstractmethod
    def Create(self, u: User) -> Exception:
        pass

    @abstractmethod
    def FindByEmail(self, string: str) -> (User, Exception):
        pass
