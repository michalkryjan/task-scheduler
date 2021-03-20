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


class Task:
    def __init__(self, name, description, deadline, is_urgent):
        self.name = name
        self.description = description
        self.deadline = deadline
        self.time_added = datetime.now()
        self.is_urgent = is_urgent
        self.status = 'new'

    def addTaskToDb(self):
        try:
            sqliteConnection = createConnection()
            db = sqliteConnection.cursor()
            db.execute("INSERT INTO tasks(name, description, deadline, is_urgent, time_added, status) VALUES (?, ?, ?, ?, ?, ?)", (str(self.name), str(self.description), str(self.deadline), str(self.is_urgent), str(self.time_added), str(self.status)))
            sqliteConnection.commit()
            print('successfully added')
        except sqlite3.Error as error:
            print("Error while adding a new task to db", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()

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
        print("Error while creating a new table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def getAllTasks():
    sqliteConnection = createConnection()
    try:
        db = sqliteConnection.cursor()
        db.execute("SELECT * FROM tasks")
        rows = db.fetchall()
        if len(rows) == 0:
            print('No tasks! Enjoy your free time :)')
        for row in rows:
            print(row)
    except sqlite3.Error as error:
        print("Error while selecting all tasks", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
