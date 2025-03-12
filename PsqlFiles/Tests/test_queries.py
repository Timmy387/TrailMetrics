from DatabaseQueries.connect import connect_trail_db_psql
from unittest import TestCase
from DatabaseQueries.trail_users_queries import *

class TestQueries(TestCase):
    def setUp(self):
        self.conn = connect_trail_db_psql()
        self.maxDiff = None

    def tearDown(self):
        self.conn.close()

    def test_trail_use_given_date(self):
        result = trail_use_given_date(conn, "03-31-2018", "Saddlemire")
        with open("Psql_files/Tests/Gold_files/gold_trail_use_given_date.txt", "r") as file:
            expected = file.read()
        self.assertEqual(result, expected.strip())
conn = connect_trail_db_psql()