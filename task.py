import sqlite3
from datetime import date, datetime
from db_actions import createConnection, startDb


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
            db.execute('UPDATE tasks SET status="new" WHERE id=?',(self.id))
        except sqlite3.Error as error:
            print("Error while setting a task as done", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()


class GetTasks:
    def __init__(self):
        startDb()

    def all(self):
        try:
            sqliteConnection = createConnection()
            db = sqliteConnection.cursor()
            db.execute('SELECT * FROM tasks WHERE status="new" ORDER BY deadline ASC, name')
            rows = db.fetchall()
        except sqlite3.Error as error:
            print('Error while selecting all tasks', error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
            tasks = []
            for row in rows:
                task = Task(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                tasks.append(task)
            return tasks
    
    def forToday(self):
        try:
            sqliteConnection = createConnection()
            db = sqliteConnection.cursor()
            today = date.today()
            db.execute('SELECT * FROM tasks WHERE deadline=? ORDER BY name', (str(today)))
            rows = db.fetchall()
        except sqlite3.Error as error:
            print('Error while selecting tasks for today', error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
            tasks = []
            for row in rows:
                task = Task(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                tasks.append(task)
            return tasks
    
    def forTomorrow(self):
        try:
            sqliteConnection = createConnection()
            db = sqliteConnection.cursor()
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            db.execute('SELECT * FROM tasks WHERE deadline=? ORDER BY name', (str(tomorrow)))
            rows = db.fetchall()
        except sqlite3.Error as error:
            print('Error while selecting tasks for tomorrow', error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
            tasks = []
            for row in rows:
                task = Task(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                tasks.append(task)
            return tasks
    
    def urgent(self):
        try:
            sqliteConnection = createConnection()
            db = sqliteConnection.cursor()
            db.execute('SELECT * FROM tasks WHERE is_urgent="yes" ORDER BY deadline ASC, name')
            rows = db.fetchall()
        except sqlite3.Error as error:
            print('Error while selecting urgent tasks', error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
            tasks = []
            for row in rows:
                task = Task(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                tasks.append(task)
            return tasks

    def notUrgent(self):
        try:
            sqliteConnection = createConnection()
            db = sqliteConnection.cursor()
            db.execute('SELECT * FROM tasks WHERE is_urgent="no" ORDER BY deadline ASC, name')
            rows = db.fetchall()
        except sqlite3.Error as error:
            print('Error while selecting not urgent tasks', error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
            tasks = []
            for row in rows:
                task = Task(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                tasks.append(task)
            return tasks

    def one(self, id):
        try:
            sqliteConnection = createConnection()
            db = sqliteConnection.cursor()
            db.execute('SELECT * FROM tasks WHERE id=?', (id))
            row = db.fetchone()
        except sqlite3.Error as error:
            print('Error while selecting the task', error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
            task = Task(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            return task
