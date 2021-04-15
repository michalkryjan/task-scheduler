import sqlite3
from datetime import date, timedelta
from .DbActions import createConnection
from .Task import Task


def getAllTasks():
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


def getForTodayTasks():
    try:
        sqliteConnection = createConnection()
        db = sqliteConnection.cursor()
        today = date.today().strftime('%d.%m.%Y')
        query = 'SELECT * FROM tasks WHERE deadline=? AND status="new" ORDER BY name, time_added ASC'
        db.execute(query, (today,))
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


def getForTomorrowTasks():
    try:
        sqliteConnection = createConnection()
        db = sqliteConnection.cursor()
        tomorrow = date.today() + timedelta(days=1)
        tomorrow = tomorrow.strftime('%d.%m.%Y')
        query = 'SELECT * FROM tasks WHERE deadline=? AND status="new" ORDER BY name, time_added ASC'
        db.execute(query, (tomorrow,))
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


def getUrgentTasks():
    try:
        sqliteConnection = createConnection()
        db = sqliteConnection.cursor()
        db.execute('SELECT * FROM tasks WHERE is_urgent="Yes" AND status="new" ORDER BY deadline ASC, name')
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


def getNotUrgentTasks():
    try:
        sqliteConnection = createConnection()
        db = sqliteConnection.cursor()
        db.execute('SELECT * FROM tasks WHERE is_urgent="No" AND status="new" ORDER BY deadline ASC, name')
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


def getDoneTasks():
    try:
        sqliteConnection = createConnection()
        db = sqliteConnection.cursor()
        db.execute('SELECT * FROM tasks WHERE status="done" ORDER BY deadline ASC, name')
        rows = db.fetchall()
    except sqlite3.Error as error:
        print('Error while selecting done tasks', error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        tasks = []
        for row in rows:
            task = Task(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            tasks.append(task)
        return tasks


def selectOneTask(id):
    try:
        sqliteConnection = createConnection()
        db = sqliteConnection.cursor()
        query = 'SELECT * FROM tasks WHERE id=?'
        db.execute(query, (id,))
        row = db.fetchone()
    except sqlite3.Error as error:
        print('Error while selecting the specified task', error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        task = Task(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        return task