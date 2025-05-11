import sqlite3
from sqlite3 import Connection
import pandas as pd


def create_counties(conn: Connection) -> bool:
    """
    creates the counties table in the trail_metrics DB
    :param conn: connection to trail_metrics DB
    :return: true if successful
    """
    create = """
        CREATE TABLE counties(
            county TEXT,
            state char(2),
            PRIMARY KEY (county, state)
            );
        """
    try:
        conn.execute(create)
        conn.commit()
        return True
    except sqlite3.OperationalError:
        # print("Table already exists.")
        conn.rollback()
        return False


def create_trail_users(conn: Connection) -> bool:
    """
    creates the trail_users table in the trail_metrics DB
    :param conn: connection to trail_metrics DB
    :return: true if successful
    """
    create = """
        CREATE TABLE trail_users(
            day DATE,
            time TEXT,
            trail_name TEXT,
            county TEXT,
            state char(2),
            group_size numeric(3,0),
            PRIMARY KEY (day, time, trail_name, county, state),
            FOREIGN KEY (trail_name, county, state) REFERENCES trails(trail_name, county, state)
        );
        """
    try:
        conn.execute(create)
        conn.commit() # commit and rollback seem unnecessary for actual DDL, included for completeness
        return True
    except sqlite3.OperationalError:
        print("Table already exists.")
        conn.rollback()
        return False


def create_trails(conn: Connection) -> bool:
    create = """
        CREATE TABLE trails (
            trail_name TEXT,
            county TEXT,
            state char(2),
            PRIMARY KEY (trail_name, county, state),
            FOREIGN KEY (county, state) REFERENCES counties(county, state)
        );
        """
    try:
        conn.execute(create)
        conn.commit()
        return True
    except sqlite3.OperationalError:
        print("This table already exists.")
        conn.rollback()
        return False


def create_files(conn: Connection) -> bool:
    create = """
        CREATE TABLE files(
            trail_name TEXT,
            county TEXT,
            state char(2),
            start_date DATE,
            end_date DATE,
            file_path TEXT,
            PRIMARY KEY (file_path),
            FOREIGN KEY (trail_name, county, state) REFERENCES trails(trail_name, county, state)
        );
        """
    try:
        conn.execute(create)
        conn.commit()
        return True
    except sqlite3.OperationalError:
        print("This table already exists.")
        conn.rollback()
        return False


def drop_table(conn: Connection, table_name: str) -> bool:
    """
    drops trail_users table from trail_metrics DB
    :param conn: connection to trail_metrics
    :param table_name: name of table to be dropped
    :return: true if successful
    """
    if not table_name.isidentifier():
        raise ValueError("Invalid table name.")
    drop = f"DROP TABLE IF EXISTS {table_name};"
    conn.execute(drop)
    conn.commit()
    return True

def states_counties_add(conn):
    url = "https://github.com/Timmy387/TrailMetrics/raw/refs/heads/main/ExtraFiles/countyState.csv"
    df = pd.read_csv(url)
    insert = """
        INSERT INTO counties VALUES (?, ?);
        """
    for index, row in df.iterrows():
        conn.execute(insert, (row['county'], row['state']))
        conn.commit()


def create_all_tables(conn: Connection) -> None:
    # check if conn has any tables in it
    check_for_tables = """
        SELECT count(*) FROM sqlite_master WHERE type='table';
        """
    if conn.execute(check_for_tables).fetchone()[0] > 0:
        return
    create_counties(conn)
    create_trails(conn)
    create_trail_users(conn)
    create_files(conn)
    states_counties_add(conn)