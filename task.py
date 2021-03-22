import sqlite3
from datetime import date, datetime
from db_actions import createConnection

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
