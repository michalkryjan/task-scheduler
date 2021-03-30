import sqlite3
import os.path
from datetime import date, datetime


def createConnection():
    conn = None
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "scheduler.db")
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
                                        is_urgent TEXT NOT NULL,
                                        time_added DATETIME NOT NULL,
                                        status TEXT NOT NULL);'''
        db.execute(create_table_query)
    except sqlite3.Error as error:
        print('Error while creating a new table', error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def addTaskToDb(name, description, deadline, is_urgent):
    try:
        time_added = datetime.now()
        status = 'new'
        sqliteConnection = createConnection()
        db = sqliteConnection.cursor()
        db.execute("INSERT INTO tasks(name, description, deadline, is_urgent, time_added, status) VALUES (?, ?, ?, ?, ?, ?)", (str(name), str(description), str(deadline), str(is_urgent), str(time_added), str(status)))
        sqliteConnection.commit()
        print('successfully added')
    except sqlite3.Error as error:
        print("Error while adding a new task to db", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

