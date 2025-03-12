from SQLiteFiles.DatabaseQueries.trail_users_queries import *
from SQLiteFiles.DatabaseQueries.trails_queries import *
from connect_sqlite import connect_trail_db_sqlite

from SQLiteFiles.DDL.create_tables import *
def create(trail_conn: Connection):
    drop_table(trail_conn, "trail_users")
    drop_table(trail_conn, "files")
    drop_table(trail_conn, "trails")
    drop_table(trail_conn, "trail_locations")
    create_trails(trail_conn)
    create_files(trail_conn)
    create_trail_users(trail_conn)
    create_trail_locations(trail_conn)


from SQLiteFiles.DDL.upload_file import *
def upload_files(trail_conn: Connection):
    remove_file_values_trail_user(trail_conn,
        "Saddlemire17_10_13-18_03_31.txt", "Saddlemire")
    upload(trail_conn,"Saddlemire17_10_13-18_03_31.txt", "Saddlemire")
    # upload(trail_conn,"Saddlemire17_02_02-17_05_04.txt", "Saddlemire")
    # upload(trail_conn,"Saddlemire17_05_04-17_09_08.txt", "Saddlemire")
    # upload(trail_conn,"Saddlemire18_04_21-19_04_24.txt", "Saddlemire")
    # upload(trail_conn,"Saddlemire19_04_24-19_09_04.txt", "Saddlemire")
    # upload(trail_conn, "Saddlemire24-10-4_24-11-26.txt", "Saddlemire")
    # upload(trail_conn, "TontoPipeCreek15_05_07-15-05-26.txt", "Tonto Pipe Creek")

def states_counties_add(conn):
    insert = """
        INSERT INTO trail_locations VALUES (?, ?);
        """
    with open("fips-by-state.csv", "r") as f:
        for line in f:
            line = line.strip().split(",")
            conn.execute(insert, (line[1], line[2]))
            conn.commit()


from SQLiteFiles.DDL.inserts import *
def trail_inserts(trail_conn: Connection):
    delete_trail(conn, "Saddlemire")
    insert_trail(trail_conn, "Saddlemire", "St. Lawrence County", "NY")
    delete_trail(trail_conn, "Tonto Pipe Creek")
    insert_trail(trail_conn, "Tonto Pipe Creek", "Gila County", "AZ")


if __name__ == '__main__':
    conn = connect_trail_db_sqlite()
    # create(conn)
    # trail_inserts(conn)
    # upload_files(conn)
    conn.close()


