import atexit

import mysql.connector

from .config import Config
from .store import sqlstore
from .server import Server


def start(config: Config):
    db = newDB(config.Database)  # TODO: check error
    store = sqlstore.Store(db)

    srv = Server(store, config.Flask)

    srv.flask.run(host="0.0.0.0")


def newDB(database_config: Config.Database) -> mysql.connector.MySQLConnection:
    db = mysql.connector.connect(**database_config)
    print('connected to database')

    def exit_handler():
        db.close()

    atexit.register(exit_handler)
    return db
