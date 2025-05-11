from sqlite3 import Connection
import sqlite3

def insert_trail_user(conn: Connection,
                      day: str, time: str,
                      trail_name: str, county: str, state: str,
                      group_size: int) -> bool:
    """
    inserts a trail user into the trail_users table
    :param conn: connection to the trail_metrics DB
    :param day: date the user was counted
    :param time: time the user was counted
    :param trail_name: trail the user was walking on
    :param county: county the trail is in
    :param state: state the trail is in
    :param group_size: number of people in the counted group
    :return: true if user was added, false otherwise
    """
    insert = """
        INSERT INTO trail_users VALUES (?, ?, ?, ?, ?, ?);
        """
    try:
        conn.execute(insert, (day, time, trail_name, county, state, group_size))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        conn.rollback()
        print("nah")
        return False


def soft_insert_trail_user(conn: Connection,
                           day: str, time: str,
                           trail_name: str, county: str, state: str,
                           group_size: int) -> bool:
    """
    inserts a trail user into the trail_users table, doesn't commit changes
    :param conn: connection to the trail_metrics DB
    :param day: date the user was counted
    :param time: time the user was counted
    :param trail_name: location the user was counted
    :param group_size: number of people in the counted group
    :return: true if user was added, false otherwise
    """
    insert = """
        INSERT INTO trail_users VALUES (?, ?, ?, ?, ?, ?);
        """
    try:
        conn.execute(insert, (day, time, trail_name, county, state, group_size))
        return True
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
        print("oops")
        return False


def delete_trail_user(conn: Connection,
                      day: str, time: str,
                      trail_name: str, county: str, state: str) -> bool:
    """
    delete a trail usage
    :param conn: connection to the trail_metrics DB
    :param day: date the user was counted
    :param time: time the user was counted
    :param trail_name: trail the user was walking on
    :param county: county the trail is in
    :param state: state the trail is in
    :return: true if successful
    """
    delete = """
        DELETE FROM trail_users WHERE day = ? 
                                    AND time = ? 
                                    AND trail_name = ?
                                    AND county = ?
                                    AND state = ?;
        """
    conn.execute(delete, (day, time, trail_name, county, state))
    conn.commit()
    return True


def insert_trail(conn: Connection, trail_name: str, county: str, state: str) -> bool:
    """
    adds a trail to the trails table
    :param conn: connection to the trail_metrics DB
    :param trail_name: name of trail to add
    :param county: county the trail is in
    :param state: state the trail is in
    :return: true if successful
    """
    check_for_trail = """
        SELECT count(*) 
        FROM trails 
        WHERE trail_name = ?
            AND county = ?
            AND state = ?;
        """
    insert = """
        INSERT INTO trails VALUES (?, ?, ?);
        """
    if conn.execute(check_for_trail, (trail_name, county, state)).fetchone()[0] > 0:
        return False
    try:
        conn.execute(insert, (trail_name, county, state))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        conn.rollback()
        return False


def delete_trail(conn: Connection, trail_name: str, county: str, state: str) -> bool:
    check_for_trail = """
        SELECT count(*) 
        FROM trails 
        WHERE trail_name = ?
            AND county = ?
            AND state = ?;
        """
    delete_users = """
        DELETE FROM trail_users WHERE trail_name = ? AND county = ? AND state = ?;
        """
    delete_files = """
        DELETE FROM files WHERE trail_name = ? AND county = ? AND state = ?;
        """
    delete = """
        DELETE FROM trails WHERE trail_name = ? AND county = ? AND state = ?;
        """
    if conn.execute(check_for_trail, (trail_name, county, state)).fetchone()[0] == 0:
        return False
    try:
        conn.execute(delete_users, (trail_name, county, state))
        conn.execute(delete_files, (trail_name, county, state))
        conn.execute(delete, (trail_name, county, state))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        conn.rollback()
        return False
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
        return False


def insert_file(conn: Connection,
                trail_name: str, county: str, state: str,
                start_date: str, end_date: str,
                file_path: str) -> bool:
    """
    adds a file that has been uploaded into the files table in the trail_metrics DB
    :param conn: connection to the trail_metrics DB
    :param trail_name: name of trail the file is storing data for
    :param county: county the trail is in
    :param state: state the trail is in
    :param start_date: date of first entry
    :param end_date: date of last entry
    :param file_path: name of .txt file
    :return: true if successful
    """
    check_for_file = """
        SELECT count(*) 
        FROM files 
        WHERE file_path = ?;
        """
    insert = """
        INSERT INTO files VALUES (?, ?, ?, ?, ?, ?);
        """
    if conn.execute(check_for_file, (file_path,)).fetchone()[0] > 0:
        return False
    try:
        conn.execute(insert, (trail_name, county, state,
                              start_date, end_date, file_path))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        conn.rollback()
        return False


def delete_file(conn: Connection, file_path: str) -> bool:
    """
    deletes a file listing from the files table
    :param conn: connection to the trail_metrics DB
    :param file_path: name of file being removed
    :return: true if successful
    """
    check_for_file = """
        SELECT count(*) 
        FROM files 
        WHERE file_path = ?;
        """
    if conn.execute(check_for_file, (file_path,)).fetchone()[0] == 0:
        return False
    delete = """
        DELETE FROM files WHERE file_path = ?;
        """
    conn.execute(delete, (file_path,))
    conn.commit()
    return True