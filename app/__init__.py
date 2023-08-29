import atexit
import logging

import mysql.connector
from mysql.connector import pooling

from .config import Config
from .store import sqlstore
from .server import Server


def start(config: Config):
    logger = new_logger(config.log_level)
    db = new_db(config.database)
    store = sqlstore.Store(db, logger)
    logger.info('connected to database (pool connections)')

    srv = Server(store, config.flask, logger)

    srv.flask.run(host="0.0.0.0", threaded=False)


def new_db(database_config: Config.database) -> mysql.connector.pooling.MySQLConnectionPool:
    connection_pool = pooling.MySQLConnectionPool(pool_name="app", pool_size=1, **database_config)

    def exit_handler():
        pass

    atexit.register(exit_handler)

    return connection_pool


def new_logger(lvl: str) -> logging.Logger:
    logger_instance = logging.getLogger('app')
    logger_instance.setLevel(logging.getLevelName(lvl))
    logger_instance.propagate = False

    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler('app.log')

    formatter = logging.Formatter('%(levelname)s[%(asctime)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger_instance.addHandler(console_handler)
    logger_instance.addHandler(file_handler)

    return logger_instance
