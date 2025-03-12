import sqlite3


def connect_trail_db_sqlite() -> sqlite3.Connection:
    """
    connects to the trail_metrics DB hosted on the local machine.
    :return: connection to the DB
    """
    try:
        conn = sqlite3.connect("../trail_metrics.db")
        conn.execute("PRAGMA foreign_keys=ON;")
        if not conn.execute("PRAGMA foreign_keys;"):
            exit(1)
    except sqlite3.DatabaseError:
        print("Database not found")
        exit(1)
    return conn