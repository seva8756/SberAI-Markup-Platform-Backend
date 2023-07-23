import mysql.connector
from mysql.connector import pooling


def TestDB(database_config) -> (mysql.connector.MySQLConnection, lambda *tables: None):
    print(database_config)
    db = pooling.MySQLConnectionPool(pool_name="app", pool_size=1, **database_config)
    print('connected to database')

    def teardown(*tables):
        if len(tables) > 0:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {', '.join(tables)}")
            conn.commit()
            cursor.close()
            conn.close()

    return db, teardown
