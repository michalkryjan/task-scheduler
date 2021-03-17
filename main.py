import sqlite3
import os.path
from datetime import date, time


class Task:
    def __init__(self, name, description, deadline):
        self.name = name
        self.description = description
        self.deadline = deadline
        self.date_added = date.today()
        self.time_added = time.now()
        self.status = 'new'

    def add_task_to_db(self):
        try:
            sqliteConnection = sqlite3.connect(DB_PATH)
            db = sqliteConnection.cursor()
            sqlite_add_task_query = f'''INSERT INTO tasks VALUES 
                                        ("{self.name}", 
                                        "{self.description}",
                                        "{self.deadline}", 
                                        "{self.date_added}", 
                                        "{self.time_added}", 
                                        "{self.status}")'''
            db.execute(sqlite_add_task_query)
            db.commit()
        except sqlite3.Error as error:
            print("Error while adding a new task to db", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "scheduler.db")

try:
    sqliteConnection = sqlite3.connect(DB_PATH)
    db = sqliteConnection.cursor()
    sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS tasks (
                                    id INTEGER PRIMARY KEY,
                                    name TEXT NOT NULL,
                                    description TEXT,
                                    deadline TEXT,
                                    date_added_text TEXT NOT NULL,
                                    time_added_text TEXT NOT NULL,
                                    status TEXT NOT NULL);'''
    db.execute(sqlite_create_table_query)

except sqlite3.Error as error:
    print("Error while creating a new table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
