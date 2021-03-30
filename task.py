import sqlite3
from dbActions import createConnection, startDb


class Task:
    def __init__(self, id, name, description, deadline, is_urgent, time_added, status):
        self.id = id
        self.name = name
        self.description = description
        self.deadline = deadline
        self.is_urgent = is_urgent
        self.time_added = time_added
        self.status = status

    def setTaskAsDone(self):
        try:
            sqliteConnection = createConnection()
            db = sqliteConnection.cursor()
            db.execute('UPDATE tasks SET status="done" WHERE id=?',(str(self.id),))
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print("Error while setting a task as done", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()

    def update(self, name, description, deadline, is_urgent):
        try:
            sqliteConnection = createConnection()
            db = sqliteConnection.cursor()
            db.execute('UPDATE tasks SET name=?, description=?, deadline=?, is_urgent=? WHERE id=?',(str(name), str(description), str(deadline), str(is_urgent), str(self.id),))
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print("Error while updating a task", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()


