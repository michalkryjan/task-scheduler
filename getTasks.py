import sqlite3
from datetime import datetime, date, timedelta
from dbActions import createConnection, startDb
from Task import Task


def getAll():
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
    
def getForToday():
    try:
        sqliteConnection = createConnection()
        db = sqliteConnection.cursor()
        today = date.today().strftime('%d.%m.%Y')
        db.execute('SELECT * FROM tasks WHERE deadline=? ORDER BY name', (str(today),))
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
    
def getForTomorrow():
    try:
        sqliteConnection = createConnection()
        db = sqliteConnection.cursor()
        tomorrow = date.today() + timedelta(days=1)
        tomorrow = tomorrow.strftime('%d.%m.%Y')
        db.execute('SELECT * FROM tasks WHERE deadline=? ORDER BY name', (str(tomorrow),))
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
    
def getUrgent():
    try:
        sqliteConnection = createConnection()
        db = sqliteConnection.cursor()
        db.execute('SELECT * FROM tasks WHERE is_urgent="Yes" ORDER BY deadline ASC, name')
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

def getNotUrgent():
    try:
        sqliteConnection = createConnection()
        db = sqliteConnection.cursor()
        db.execute('SELECT * FROM tasks WHERE is_urgent="No" ORDER BY deadline ASC, name')
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

def getDone():
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

def getOne(id):
    try:
        sqliteConnection = createConnection()
        db = sqliteConnection.cursor()
        db.execute('SELECT * FROM tasks WHERE id=?', (str(id)))
        row = db.fetchone()
    except sqlite3.Error as error:
        print('Error while selecting the specified task', error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        task = Task(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        return task