from typing import List

from app.model import User
from .userrepository import UserRepository


class Store:
    user_repository: UserRepository = None

    def User(self) -> UserRepository:
        if self.user_repository is not None:
            return self.user_repository

        self.user_repository = UserRepository(self, {})
        return self.user_repository
