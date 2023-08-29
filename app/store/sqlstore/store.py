import logging

import mysql.connector
from tabulate import tabulate

import app.store.store as store
from app.store.sqlstore.repositories.projectrepository.project_repository import ProjectRepository
from app.store.sqlstore.repositories.userrepository.user_repository import UserRepository
from app.store.sqlstore.repositories.tokenrepository.token_repository import TokenRepository


class QueryInfo:
    rows_affected: int = 0
    last_row_id: int = 0

    def __init__(self, rows_affected: int, last_row_id: int):
        self.rows_affected = rows_affected
        self.last_row_id = last_row_id


class Store(store.Store):
    connection_pool: mysql.connector.pooling.MySQLConnectionPool
    logger: logging.Logger
    user_repository: UserRepository = None
    token_repository: TokenRepository = None
    project_repository: ProjectRepository = None

    def __init__(self, connection_pool: mysql.connector.pooling.MySQLConnectionPool, logger: logging.Logger):
        self.connection_pool = connection_pool
        self.logger = logger

    def query(self, query: str, *args, one=False) -> (any, Exception, QueryInfo):
        def row_to_dict(columns, row):
            return dict(zip(columns, row))

        connection = None
        results = None
        info = None
        try:
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor()
            cursor.execute(query, args)
            if cursor.description:
                columns = [column[0] for column in cursor.description]
                if one:
                    row = cursor.fetchone()
                    if row:
                        results = row_to_dict(columns, row)
                else:
                    results = [row_to_dict(columns, row) for row in cursor.fetchall()]
                    
            info = QueryInfo(rows_affected=cursor.rowcount, last_row_id=cursor.lastrowid)
            while cursor.nextset():
                pass
            connection.commit()
            cursor.close()
        except Exception as err:
            return None, err, None
        finally:
            connection.close()
            self.logger.info(tabulate(
                [[query, str(args)[:100], results, vars(info) if info else ""]],
                headers=["Запрос", "Аргументы", "Результат", "Информация по запросу"]))
        return results, None, info

    def User(self) -> UserRepository:
        if self.user_repository is not None:
            return self.user_repository

        self.user_repository = UserRepository(self)
        return self.user_repository

    def Token(self) -> TokenRepository:
        if self.token_repository is not None:
            return self.token_repository

        self.token_repository = TokenRepository(self)
        return self.token_repository

    def Project(self) -> ProjectRepository:
        if self.project_repository is not None:
            return self.project_repository

        self.project_repository = ProjectRepository(self)
        return self.project_repository
