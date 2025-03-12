import csv
import sqlite3
from sqlite3 import Connection
from SQLiteFiles.DDL.inserts import (
    soft_insert_trail_user, delete_trail_user, insert_file, delete_file)
from connect_sqlite import connect_trail_db_sqlite


def upload(conn: Connection,
           trail_name: str, county: str, state: str,
           file_path: str) -> bool:
    """
    uploads a .txt file containing trail info to the trail_metrics DB
    :param conn: connection to trail tests DB
    :param trail_name: name of trail that data is from
    :param county: county that trail is in
    :param state: state that trail is in
    :param file_path: path to file to be uploaded
    :return: true if upload was successful, false otherwise
    """

    formatted_date = ""
    start_date = ""
    try:
        with open(file_path, "r") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row and row[0].startswith("=START"):
                    start_date = row[0][-8:]
                if row and row[0][0] in "1234567890":
                    formatted_date = '20' + row[0]
                    if not soft_insert_trail_user(conn, formatted_date, row[1],
                                               trail_name, county, state, int(row[2])):
                        conn.rollback()
                        return False
        insert_file(conn, trail_name, county, state, start_date, formatted_date, file_path)
        conn.commit()
        return True
    except sqlite3.OperationalError:
        print("This table doesn't exist.")
        conn.rollback()
        return False
    except FileNotFoundError:
        print("File not found.")
        conn.rollback()
        return False
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
        return False


def remove_file_values_trail_user(conn: Connection, file_path: str,
                                  trail_name: str, county: str, state: str) -> bool:
    """
    removes all values in a file from trail_user
    :param conn: connection to trail_metrics DB
    :param file_path: name of file
    :param trail_name: name of trail that file was for
    :param county: county that trail is in
    :param state: state that trail is in
    :return:
    """
    try:
        with open(file_path, "r") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row and row[0][0] in "1234567890":
                    formatted_date: str = "20" + row[0]
                    if not delete_trail_user(conn, formatted_date, row[1],
                                             trail_name, county, state):
                        conn.rollback()
                        return False
        delete_file(conn, file_path)
        conn.commit()
        return True
    except sqlite3.OperationalError:
        print("This table doesn't exist.")
        conn.rollback()
        return False
    except FileNotFoundError:
        print("File not found.")
        conn.rollback()
        return False


if __name__ == "__main__":
    conn = connect_trail_db_sqlite()
    upload(conn, "Test", "Montgomery County", "MD",
            "C:/Users/timmy/Repos/TrailMetrics/Python/Text_import_files/"
                      "Saddlemire17_10_13-18_03_31.txt")
    conn.close()