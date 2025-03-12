import sqlite3
import os


def connect_trail_db_sqlite(path:str="trail_metrics.db") -> sqlite3.Connection:
    """
    connects to the trail_metrics DB hosted on the local machine.
    :return: connection to the DB
    """
    try:
        root_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(root_dir, path)
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA foreign_keys=ON;")
        if not conn.execute("PRAGMA foreign_keys;"):
            exit(1)
    except sqlite3.DatabaseError:
        print("Database not found")
        exit(1)
    return conn