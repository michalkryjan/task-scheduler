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
            return rows
    
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
            return rows
    
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
            return rows
    
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
            return rows

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
            return rows
