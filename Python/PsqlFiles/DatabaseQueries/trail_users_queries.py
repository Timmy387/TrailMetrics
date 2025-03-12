from psycopg import Connection
from tabulate import tabulate
from Aggregating_objects.trail_user import Trail_User
def trail_use_given_date(conn: Connection, day: str, location: str) -> str:
    """
    generates a list of all users of a given trail on a specific day
    :param conn: connection to the trail_tests database
    :param day: date to be listed
    :param location: location to be checked
    :return: count of users and table of usage
    """
    count_query = """
        SELECT count(*)
        FROM trail_users
        WHERE day = %s AND lower(location) = lower(%s);
        """
    table_query = """
        SELECT time, group_size
        FROM trail_users
        WHERE day = %s AND location = %s
        ORDER BY time;
        """
    if conn.broken:
        exit(1)

    with conn.cursor() as cursor:
        cursor.execute(table_query, (day, location))
        rs = cursor.fetchall()
    table = tabulate(rs, headers=["Time Of Day", "Passersby"], tablefmt="psql")
    return table