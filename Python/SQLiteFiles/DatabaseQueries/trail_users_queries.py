from sqlite3 import Connection

from tabulate import tabulate

from util import dow_number


def trail_users_by_date(conn: Connection, date: str) -> str:
    """
    returns number of trail users on a given date on all trails
    :param conn:
    :param date:
    :return: table of users
    """
    query = """
        SELECT trail_name, sum(group_size)
        FROM trail_users
        WHERE day = ?
        GROUP BY trail_name
        UNION
        SELECT trail_name, 0
        FROM trails
        WHERE trail_name NOT IN (SELECT trail_name
                            FROM trail_users
                            WHERE day = '2018-05-11'
                            GROUP BY trail_name);
        """
    cursor = conn.cursor()
    cursor.execute(query, (date,))
    result = cursor.fetchall()
    if result:
        table = tabulate(result, headers=["Trail Name", "Users"], tablefmt="SQLite")
        return table + "\n"
    else:
        return "Query failed."

def trail_users_by_year_given_trail(conn: Connection, trail_name: str) -> str:
    """

    :param conn:
    :param trail_name:
    :return:
    """
    query = """
        SELECT trail_name, strftime('%Y', day), sum(group_size)
        FROM trail_users
        WHERE trail_name = ?
        GROUP BY trail_name, strftime('%Y', day);
        """
    cursor = conn.cursor()
    cursor.execute(query, (trail_name,))
    result = cursor.fetchall()
    if result:
        table = tabulate(result, headers=["Trail Name", "Year", "Count"], tablefmt="SQLite")
        return table + "\n"
    else:
        return "Query failed."


def trail_users_by_month_given_trail_and_year(conn: Connection, trail_name: str, year: str) -> str:
    """
    generates users by month for a given trail in a given year
    :param conn:
    :param trail_name:
    :param year: year to display
    :return: table of users by month
    """
    query = """
        SELECT trail_name, strftime('%m', day), sum(group_size)
        FROM trail_users
        WHERE trail_name = ? AND strftime('%Y', day) = ?
        GROUP BY trail_name, strftime('%m', day);
        """
    cursor = conn.cursor()
    cursor.execute(query, (trail_name, year))
    result = cursor.fetchall()
    months = [('January', '01'), ('February', '02'), ('March', '03'),
              ('April', '04'), ('May', '05'), ('June', '06'),
              ('July', '07'), ('August', '08'), ('September', '09'),
              ('October', '10'), ('November', '11'), ('December', '12')]
    if result:
        result2 = [[attribute for attribute in result[i]] for i in range(len(result))]
        # for loop makes sure months with zero users are still displayed
        for i in range(len(months)):
            if i < len(result2) and result2[i][1] == months[i][1]:
                result2[i][1] = months[i][0]
            else:
                result2.insert(i, [trail_name, months[i][0], 0])
        table = tabulate(result2, headers=["Trail Name", f"Month ({year})", "Count"], tablefmt="SQLite")
        return table + "\n"
    else:
        return "Query failed."


def avg_users_by_month_given_trail(conn: Connection, ):
    """

    :param conn:
    :return:
    """


from datetime import date
def daily_use_by_week_given_trail(conn: Connection, trail_name: str, start_date: str, end_date: str = None) -> str:
    """
    find use by day of the week for a given trail over a period of time
    :param conn:
    :param trail_name:
    :param start_date:
    :param end_date:
    :return: table of averages for seven days of the week
    """

    if end_date is None:
        end_date = date.today()

    query = """
        WITH
            diff AS
                (SELECT (julianday(?) - julianday(?)) / 7 AS day_diff)
        SELECT trail_name,
            CASE strftime('%w', day)
                WHEN '0' THEN 'Sunday'
                WHEN '1' THEN 'Monday'
                WHEN '2' THEN 'Tuesday'
                WHEN '3' THEN 'Wednesday'
                WHEN '4' THEN 'Thursday'
                WHEN '5' THEN 'Friday'
                WHEN '6' THEN 'Saturday'
            END AS day_of_week,
            round(count(*) / day_diff, 1) AS avg_users
        FROM trail_users, diff
        WHERE trail_name = ?
            AND day >= ?
            AND day <= ?
        GROUP BY strftime('%w', day);
        """
    cursor = conn.execute(query, (end_date, start_date, trail_name, start_date, end_date))
    result = cursor.fetchall()
    if result:
        table = tabulate(result, headers=["Trail Name", "Day of Week", "Avg Users"], tablefmt="SQLite")
        return table + "\n"

    else:
        return "Query failed"


def usage_by_time_of_day_by_dow(conn: Connection, trail_name: str, dow: str, start_date: str, end_date: str = None) -> str:
    """
    finds avg users by period of day for a given day of the week
    :param conn:
    :param trail_name:
    :param dow: day of week
    :param start_date:
    :param end_date:
    :return:
    """
    dow_num = dow_number(dow)

    if end_date is None:
        end_date = date.today()
    query = """
        WITH dow_entries AS (
                SELECT day as weekday,
                       trail_name,
                       CASE
                            WHEN time > '05:00:00' AND time <= '10:00:00' THEN 'Morning'
                            WHEN time > '10:00:00' AND time <= '16:00:00' THEN 'Afternoon'
                            WHEN time > '16:00:00' AND time <= '21:00:00' THEN 'Evening'
                            ELSE 'Night'
                        END AS tod
                FROM trail_users
                WHERE strftime('%w', day) = ?
                    AND day >= ?
                    AND day <= ?
                    AND trail_name = ?),
                diff AS
                (SELECT (julianday(?) - julianday(?)) / 7 AS weeks)
        SELECT trail_name, tod, round(count(tod) / weeks, 1) as users_per_week
        FROM dow_entries, diff
        GROUP BY tod, trail_name;
        """
    cursor = conn.execute(query, (dow_num, start_date,
                                  end_date, trail_name, end_date, start_date))
    result = cursor.fetchall()
    if result:
        table = tabulate(result, headers=["Trail Name", f"Time of Day ({dow})", "Users"], tablefmt="SQLite")
        return table + "\n"
    return "Query failed"