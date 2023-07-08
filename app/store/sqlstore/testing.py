import mysql.connector


def TestDB(database_config) -> (mysql.connector.MySQLConnection, lambda *tables: None):
    print(database_config)
    db = mysql.connector.connect(**database_config)
    print('connected to database')

    def teardown(*tables):
        if len(tables) > 0:
            cursor = db.cursor()
            cursor.execute(f"TRUNCATE {', '.join(tables)}")
            db.commit()
            cursor.close()
            db.close()

    return db, teardown
