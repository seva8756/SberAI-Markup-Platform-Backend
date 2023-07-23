import atexit

import mysql.connector
from mysql.connector import pooling

from .config import Config
from .store import sqlstore
from .server import Server


def start(config: Config):
    db = new_db(config.Database)
    store = sqlstore.Store(db)

    srv = Server(store, config.Flask)

    srv.flask.run(host="0.0.0.0")


def new_db(database_config: Config.Database) -> mysql.connector.pooling.MySQLConnectionPool:
    connection_pool = pooling.MySQLConnectionPool(pool_name="app", pool_size=8, **database_config)

    print('connected to database (pool connections)')

    def exit_handler():
        pass

    atexit.register(exit_handler)

    return connection_pool
