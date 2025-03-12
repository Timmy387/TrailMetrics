import csv
from psycopg import Connection
from PsqlFiles.DML.inserts import soft_insert_trail_user


def upload(conn: Connection, file_path: str, trail_name: str) -> bool:
    """
    uploads a .txt file containing trail info to the trail_tests database
    :param conn: connection to trail tests DB
    :param file_path: path to file to be uploaded
    :param trail_name: name of trail that data is from
    :return: true if upload was successful, false otherwise
    """
    with open(file_path, "r") as file:
        csv_reader = csv.reader(file)
        b: bool = True
        for row in csv_reader:
            if row and row[0][0] in "1234567890":
                format_date: str = row[0][3:5] + "-" + row[0][6:] + "-" + '20' + row[0][:2]
                b = soft_insert_trail_user(conn, format_date, row[1], trail_name, int(row[2])) and b
                if not b:
                    conn.rollback()
                    return False
    conn.commit()
    return True