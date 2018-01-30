import atexit
import sqlite3
from dbtools import Dao


class Task(object):
    def __init__(self, task_name, worker_id, resource_name, resource_amount, time_to_make,):
        self.task_name = task_name
        self.worker_id = int(worker_id)
        self.time_to_make = int(time_to_make)
        self.resource_name = resource_name
        self.resource_amount = int(resource_amount)


class Worker(object):
    def __init__(self, id, name, status):
        self.id = int(id)
        self.name = name
        self.status = status


class Resource(object):
    def __init__(self, name, amount):
        self.name = name
        self.amount = int(amount)


# Repository
class _Repository(object):
    def __init__(self):
        self._conn = sqlite3.connect('world.db')
        self._conn.text_factory = str
        self.tasks = Dao(Task, self._conn)
        self.workers = Dao(Worker, self._conn)
        self.resources = Dao(Resource, self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        try:
            self._conn.executescript("""
                CREATE TABLE tasks (
                    id INTEGER PRIMARY KEY,
                    task_name TEXT NOT NULL,
                    worker_id INTEGER REFERENCES workers(id),
                    time_to_make INTEGER NOT NULL,
                    resource_name TEXT NOT NULL,
                    resource_amount INTEGER NOT NULL
                );
                CREATE TABLE workers (
                   id INTEGER PRIMARY KEY,
                   name TEXT NOT NULL,
                   status TEXT NOT NULL    
                );
                CREATE TABLE resources (
                   name TEXT PRIMARY KEY,
                   amount INTEGER NOT NULL
                );
            """)
        except sqlite3.OperationalError:
            # if the tables already exist
            pass


# singleton
repo = _Repository()
atexit.register(repo._close)