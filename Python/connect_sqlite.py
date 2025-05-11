import sqlite3
import os
from SQLiteFiles.DDL.create_tables import create_all_tables


def connect_trail_db_sqlite(path:str="trail_metrics.db") -> sqlite3.Connection:
    """
    connects to the trail_metrics DB hosted on the local machine.
    :return: connection to the DB
    """
    try:
        DB_DIR = os.path.join(os.getenv("APPDATA"), "TrailMetrics", "Files")
        DB_PATH = os.path.join(DB_DIR, "trail_metrics.db")
        # root_dir = os.path.dirname(os.path.abspath(__file__))
        # db_path = os.path.join(root_dir, path)
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys=ON;")
        if not conn.execute("PRAGMA foreign_keys;"):
            exit(1)
        create_all_tables(conn)
    except sqlite3.DatabaseError:
        print("Database not found")
        exit(1)
    return conn