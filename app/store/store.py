from abc import abstractmethod

import mysql.connector
from .repository import UserRepository


class Store:

    @abstractmethod
    def User(self) -> UserRepository:
        pass
