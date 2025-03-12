from sqlite3 import Connection
from tabulate import tabulate

def list_trails(conn: Connection) -> str:
    """
    lists all trails that have been stored
    :param conn:
    :return: string list of trails
    """
    query = """
        SELECT *
        FROM trails;
        """
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    if result:
        table = tabulate(result, headers=["Trail Name", "County", "State"], tablefmt="SQLite")
        return table + "\n"
    else:
        return "Query failed."

def is_trail(conn: Connection, trail_name: str) -> bool:
    """
    checks if a trail exists in the database
    :param conn:
    :param trail_name:
    :return: boolean
    """
    query = """
        SELECT *
        FROM trails
        WHERE lower(trail_name) = lower(?);
        """
    cursor = conn.cursor()
    cursor.execute(query, (trail_name,))
    result = cursor.fetchall()
    if result:
        return True
    return False