from sqlite3 import Connection


def is_state(conn: Connection, state: str) -> bool:
    query = """
        SELECT state
        FROM trail_locations
        WHERE lower(state) = lower(?);
        """
    cursor = conn.cursor()
    cursor.execute(query, (state,))
    result = cursor.fetchall()
    if result:
        return True
    else:
        return False

def is_county_in_state(conn, county: str, state: str) -> bool:
    query = """
        SELECT county
        FROM trail_locations
        WHERE lower(county) = lower(?) AND lower(state) = lower(?);
        """
    cursor = conn.cursor()
    cursor.execute(query, (county, state))
    result = cursor.fetchall()
    if result:
        return True
    else:
        return False