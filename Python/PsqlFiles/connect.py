import psycopg


def connect_trail_db_psql() -> psycopg.Connection: # type hint

    pgpass_file = None # file handler/object
    # secure coding practice: always ask what can go wrong
    try:
        pgpass_file = open("C:/Users/Timmy/.pwd_ada")
    except OSError:
        print("Error: authorization failed.")
        exit(2)
    try:
        conn = psycopg.connect(
            dbname = "trail_tests", # named parameter, don't have to worry about the order of arguments
            user = "tboyc21",
            host = "ada.hpc.stlawu.edu",
            password = pgpass_file.readline().strip()
        )
        pgpass_file.close()
    except psycopg.Error:
        print("Error: cannot connect.")
        exit(3)
    finally:
        pgpass_file.close()

    return conn
