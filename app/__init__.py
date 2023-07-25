import atexit

import mysql.connector
from mysql.connector import pooling

from .config import Config
from .store import sqlstore
from .server import Server


def start(config: Config):
    db = new_db(config.database)
    store = sqlstore.Store(db)

    srv = Server(store, config.flask)

    srv.flask.run(host="0.0.0.0", threaded=False)


def new_db(database_config: Config.database) -> mysql.connector.pooling.MySQLConnectionPool:
    connection_pool = pooling.MySQLConnectionPool(pool_name="app", pool_size=1, **database_config)

    print('connected to database (pool connections)')

    def exit_handler():
        pass

    atexit.register(exit_handler)

    return connection_pool
