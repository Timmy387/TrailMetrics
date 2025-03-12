import psycopg.errors
from psycopg import Connection

def insert_trail_user(conn: Connection, day: str, time: str, location: str, group_size: int) -> bool:
    """
    inserts a trail user into the trail_users table
    :param conn: connection to the trail_tests database
    :param day: date the user was counted
    :param time: time the user was counted
    :param location: location the user was counted
    :param group_size: number of people in the counted group
    :return: true if user was added, false otherwise
    """
    insert = """
        INSERT INTO trail_users VALUES (%s, %s, %s, %s);
        """
    if conn.broken:
        exit(1)
    try:
        conn.execute(insert, (day, time, location, group_size))
        conn.commit()
    except psycopg.errors.UniqueViolation:
        conn.rollback()
        return False
    return True

def delete_trail_user(conn: Connection, day: str, time: str, location: str) -> bool:
    delete = """
        DELETE FROM trail_users WHERE day = %s AND time = %s AND location = %s;
        """
    if conn.broken:
        exit(1)
    conn.execute(delete, (day, time, location))
    conn.commit()

def soft_insert_trail_user(conn: Connection, day: str, time: str, location: str, group_size: int) -> bool:
    """
    inserts a trail user into the trail_users table
    :param conn: connection to the trail_tests database
    :param day: date the user was counted
    :param time: time the user was counted
    :param location: location the user was counted
    :param group_size: number of people in the counted group
    :return: true if user was added, false otherwise
    """
    insert = """
        INSERT INTO trail_users VALUES (%s, %s, %s, %s);
        """
    if conn.broken:
        exit(1)
    try:
        conn.execute(insert, (day, time, location, group_size))
    except psycopg.errors.UniqueViolation:
        return False
    return True