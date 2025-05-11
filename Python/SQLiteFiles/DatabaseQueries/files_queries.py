from sqlite3 import Connection

def get_all_files(conn: Connection):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM files")
    result = cursor.fetchall()
    if result:
        return result
    return None


def is_file(conn: Connection, file_path: str):
    query = """
        SELECT * FROM files WHERE file_path = ?;
        """
    cursor = conn.cursor()
    cursor.execute(query, (file_path,))
    # check if result has any files listed
    result = cursor.fetchall()
    return result != []