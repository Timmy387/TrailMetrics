import psycopg.errors
from psycopg import Connection
from PsqlFiles.connect import connect_trail_db_psql

def create_trail_users(conn: Connection) -> bool:
    create = """
        CREATE TABLE trail_users(
            day DATE,
            time TEXT,
            location TEXT,
            group_size numeric(3,0),
            primary key (day, time, location)
        );
        """
    if conn.broken:
        exit(1)
    try:
        conn.execute(create)
        conn.commit()
    except psycopg.errors.DuplicateTable:
        conn.rollback()
        return False
    return True

def drop_trail_users(conn: Connection) -> bool:
    drop = """
        DROP TABLE IF EXISTS trail_users;
        """
    if conn.broken:
        exit(1)
    conn.execute(drop)
    conn.commit()
    return True

if __name__ == "__main__":
    conn = connect_trail_db_psql()
    drop_trail_users(conn)
    create_trail_users(conn)