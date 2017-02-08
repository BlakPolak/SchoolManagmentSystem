import sqlite3
class Data:
    db = "program.db"

    def __init__(self):
        pass

    @classmethod
    def init_db(cls):
        data = sqlite3.connect(cls.db)
        cursor = data.cursor()
        return cursor
