import sqlite3
import os.path


def createConnection():
    conn = None
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "Tasks.db")
    try:
        conn = sqlite3.connect(DB_PATH)
    except sqlite3.Error as e:
        print(e)
    return conn


def startDb():
    sqliteConnection = createConnection()
    try:
        db = sqliteConnection.cursor()
        create_table_query = '''CREATE TABLE IF NOT EXISTS tasks (
                                        id INTEGER PRIMARY KEY,
                                        name TEXT NOT NULL,
                                        description TEXT,
                                        deadline DATETIME NOT NULL,
                                        priority TEXT NOT NULL,
                                        status TEXT NOT NULL);'''
        db.execute(create_table_query)
    except sqlite3.Error as error:
        print('Error while creating a new table', error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def addTaskToDb(name, description, deadline, priority):
    try:
        status = 'new'
        sqliteConnection = createConnection()
        db = sqliteConnection.cursor()
        query = "INSERT INTO tasks(name, description, deadline, priority, status) VALUES (?, ?, ?, ?, ?)"
        db.execute(query, (name, description, deadline, priority, status))
        sqliteConnection.commit()
    except sqlite3.Error as error:
        print("Error while adding a new task to db", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
