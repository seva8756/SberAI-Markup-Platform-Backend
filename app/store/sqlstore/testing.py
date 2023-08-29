import logging

import mysql.connector
from mysql.connector import pooling

from app.store.sqlstore import Store
from app.store.sqlstore.test_store import get_test_database_config


def TestDB(database_config=get_test_database_config()) -> (mysql.connector.MySQLConnection, lambda *tables: None):
    db = pooling.MySQLConnectionPool(pool_name="app", pool_size=1, **database_config)

    def teardown(*tables):
        if len(tables) > 0:
            conn = db.get_connection()
            cursor = conn.cursor()
            for table in tables:
                cursor.execute(f"DELETE FROM {table}")
            conn.commit()
            cursor.close()
            conn.close()

    return db, teardown


def TestStore() -> (Store, lambda *tables: None):
    db, teardown = TestDB()
    s = Store(db, logging.Logger("test", "DEBUG"))
    return s, teardown
