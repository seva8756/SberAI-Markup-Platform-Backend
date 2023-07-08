import mysql.connector
import app.store.store as store
from .userrepository import UserRepository


class Store(store.Store):
    db: mysql.connector.MySQLConnection
    user_repository: UserRepository = None

    def __init__(self, db: mysql.connector.MySQLConnection):
        self.db = db

    def query(self, query: str, *args) -> (any, Exception):
        try:
            cursor = self.db.cursor()
            print(f"Args: {args}")
            cursor.execute(query, args)

            results = cursor.fetchall()
            print(f"Results: {results}")
            self.db.commit()
            cursor.close()
        except Exception as err:
            return None, err
        return results, None

    def User(self) -> UserRepository:
        if self.user_repository is not None:
            return self.user_repository

        self.user_repository = UserRepository(self)
        return self.user_repository
