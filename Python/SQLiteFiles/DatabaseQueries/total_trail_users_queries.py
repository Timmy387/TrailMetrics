from sqlite3 import Connection


def fill_results(results, full_list):
    res_i = 0
    new_list = []
    for i, num in enumerate(full_list):
        count = 0
        if len(results) > res_i:
            res_num, res_count = results[res_i]
        else:
            res_num, res_count = None, 0
        if num == res_num:
            count = res_count
            res_i += 1
        new_list.append((num, count))
    return new_list


def per_month_each_year(conn: Connection,
                        trail_name: str, county: str, state: str,
                        start_date: str, end_date: str) -> list:
    """

    :param conn:
    :param trail_name:
    :param county:
    :param state:
    :param start_date: start date to display
    :param end_date: end date to display
    :return:
    """

    query = """
        SELECT strftime('%m', day), count(*)
        FROM trail_users
        WHERE trail_name = ?
            AND county = ?
            AND state = ?
            AND day >= ?
            AND day <= ?
        GROUP BY strftime('%m', day);
        """
    cursor = conn.cursor()
    cursor.execute(query, (trail_name, county, state, start_date, end_date))
    result = cursor.fetchall()
    i = 0
    # Format the result to include month names instead of just numbers
    months = [('01', 'January'), ('02', 'February'), ('03', 'March'),
                ('04', 'April'), ('05', 'May'), ('06', 'June'),
                ('07', 'July'), ('08', 'August'), ('09', 'September'),
                ('10', 'October'), ('11', 'November'), ('12', 'December')]
    new_result = []
    res = 0
    for i, tup in enumerate(months):
        num, month = tup
        count = 0
        if len(result) > res:
            res_num, res_count = result[res]
        else:
            res_num, res_count = None, 0
        if num == res_num:
            count = res_count
            res += 1
        new_result.append((month, count))
    return new_result


def per_week_each_year(conn: Connection,
                       trail_name: str, county: str, state: str,
                       start_date: str, end_date: str) -> list:
        """
        find total users for a given trail by week over a period of time
        :param conn:
        :param trail_name:
        :param county:
        :param state:
        :param start_date: start date to display
        :param end_date: end date to display
        :return:
        """

        query = """
            SELECT strftime('%W', day), count(*)
            FROM trail_users
            WHERE trail_name = ?
                AND county = ?
                AND state = ?
                AND day >= ?
                AND day <= ?
            GROUP BY strftime('%W', day);
            """
        cursor = conn.cursor()
        cursor.execute(query, (trail_name, county, state, start_date, end_date))
        result = cursor.fetchall()
        weeks = [f"{i:02}" for i in range(0, 54)]
        new_result = fill_results(result, weeks)
        return new_result


def per_day_of_year_each_year(conn: Connection,
                              trail_name: str, county: str, state: str,
                              start_date: str, end_date: str) -> list:
    """
    find total users for a given trail by day over a period of time
    :param conn:
    :param trail_name:
    :param county:
    :param state:
    :param start_date: start date to display
    :param end_date: end date to display
    :return:
    """

    query = """
        SELECT strftime('%m-%d', day), count(*)
        FROM trail_users
        WHERE trail_name = ?
            AND county = ?
            AND state = ?
            AND day >= ?
            AND day <= ?
        GROUP BY strftime('%m-%d', day);
        """
    cursor = conn.cursor()
    cursor.execute(query, (trail_name, county, state, start_date, end_date))
    result = cursor.fetchall()
    # figure out month of start date and end date

    days = []
    for i in range(1, 13):
        if i == 2:
            days += [f"{i:02}-{j:02}" for j in range(1, 29)]
        elif i in [4, 6, 9, 11]:
            days += [f"{i:02}-{j:02}" for j in range(1, 31)]
        else:
            days += [f"{i:02}-{j:02}" for j in range(1, 32)]
    new_result = fill_results(result, days)
    return new_result


def per_day_of_week_each_year(conn: Connection,
                              trail_name: str, county: str, state: str,
                              start_date: str, end_date: str) -> list:
    """
    find total users for a given trail by day of the week over a period of time
    :param conn:
    :param trail_name:
    :param county:
    :param state:
    :param start_date: start date to display
    :param end_date: end date to display
    :return:
    """

    query = """
        SELECT strftime('%w', day), count(*)
        FROM trail_users
        WHERE trail_name = ?
            AND county = ?
            AND state = ?
            AND day >= ?
            AND day <= ?
        GROUP BY strftime('%w', day);
        """
    cursor = conn.cursor()
    cursor.execute(query, (trail_name, county, state, start_date, end_date))
    result = cursor.fetchall()
    days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    new_result = []
    res_i = 0
    for i, day in enumerate(days_of_week):
        count = 0
        if len(result) > res_i:
            res_num, res_count = result[res_i]
        else:
            res_num, res_count = None, 0
        if str(i) == res_num:
            count = res_count
            res_i += 1
        new_result.append((day, count))
    return new_result


def per_time_of_day_each_year(conn: Connection,
                              trail_name: str, county: str, state: str,
                              start_date: str, end_date: str) -> list:
    """
    find total users for a given trail by time of day over a period of time
    :param conn:
    :param trail_name:
    :param county:
    :param state:
    :param start_date: start date to display
    :param end_date: end date to display
    :return:
    """

    query = """        
        SELECT CASE
                WHEN time > '05:00:00' AND time <= '08:00:00' THEN 'Early Morning\n(5am - 8am)'
                WHEN time > '08:00:00' AND time <= '11:00:00' THEN 'Late Morning\n(8am - 11am)'
                WHEN time > '11:00:00' AND time <= '14:00:00' THEN 'Early Afternoon\n(11am - 2pm)'
                WHEN time > '14:00:00' AND time <= '17:00:00' THEN 'Late Afternoon\n(2pm - 5pm)'
                WHEN time > '17:00:00' AND time <= '20:00:00' THEN 'Early Evening\n(5pm - 8pm)'
                WHEN time > '20:00:00' AND time <= '23:00:00' THEN 'Late Evening\n(8pm - 11pm)'
                ELSE 'Night\n(11pm - 5am)'
            END AS tod,
               count(*)
        FROM trail_users
            WHERE trail_name = ?
            AND county = ?
            AND state = ?
            AND day >= ?
            AND day <= ?
        GROUP BY tod;
        """
    cursor = conn.cursor()
    cursor.execute(query, (trail_name, county, state, start_date, end_date))
    result = cursor.fetchall()
    times = ["Early Afternoon\n(11am - 2pm)", "Early Evening\n(5pm - 8pm)", "Early Morning\n(5am - 8am)",
             "Late Afternoon\n(2pm - 5pm)", "Late Evening\n(8pm - 11pm)", "Late Morning\n(8am - 11am)", "Night\n(11pm - 5am)"]
    new_result = fill_results(result, times)
    new_result = [new_result[i] for i in [2, 5, 0, 3, 1, 4, 6]]
    return new_result


def per_day_of_year_each_month(conn: Connection,
                                 trail_name: str, county: str, state: str,
                                 start_date: str, end_date: str) -> list:
        """
        find total users for a given trail by day over a period of time
        :param conn:
        :param trail_name:
        :param county:
        :param state:
        :param start_date: start date to display
        :param end_date: end date to display
        :return:
        """

        query = """
            SELECT strftime('%m-%d', day), count(*)
            FROM trail_users
            WHERE trail_name = ?
             AND county = ?
             AND state = ?
             AND day >= ?
             AND day <= ?
            GROUP BY strftime('%m-%d', day);
            """
        cursor = conn.cursor()
        cursor.execute(query, (trail_name, county, state, start_date, end_date))
        result = cursor.fetchall()
        start_month = int(start_date.split("-")[1])
        end_month = int(end_date.split("-")[1])
        days = []
        for i in range(start_month, end_month + 1):
            if i == 2:
                days += [f"{i:02}-{j:02}" for j in range(1, 29)]
            elif i in [4, 6, 9, 11]:
                days += [f"{i:02}-{j:02}" for j in range(1, 31)]
            else:
                days += [f"{i:02}-{j:02}" for j in range(1, 32)]
        new_result = fill_results(result, days)
        return new_result

