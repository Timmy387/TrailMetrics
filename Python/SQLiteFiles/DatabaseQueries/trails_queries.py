from sqlite3 import Connection
from tabulate import tabulate

def list_trails(conn: Connection):
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
    tuples = cursor.fetchall()

    if tuples:
        result = []
        for tup in tuples:
            result.append(tup[0] + ", " + tup[1] + ", " + tup[2])
        return result
        # table = tabulate(result, headers=["Trail Name", "County", "State"], tablefmt="SQLite")
        # return table + "\n"
    else:
        return None

def is_trail(conn: Connection, trail_name: str, county: str, state: str) -> bool:
    """
    checks if a trail exists in the database
    :param conn:
    :param trail_name:
    :param county:
    :param state:
    :return: boolean
    """
    query = """
        SELECT *
        FROM trails
        WHERE trail_name = ?
            AND county = ?
            AND state = ?;
        """
    cursor = conn.cursor()
    cursor.execute(query, (trail_name, county, state))
    result = cursor.fetchall()
    return result != []