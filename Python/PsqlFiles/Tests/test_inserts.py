from unittest import TestCase
from PsqlFiles.DDL.inserts import *
from PsqlFiles.connect import connect_trail_db_psql

class TestInserts(TestCase):
    def setUp(self):
        self.conn = connect_trail_db_psql()

    def tearDown(self):
        self.conn.close()

    def test_insert_trail_user(self):
        delete_trail_user(self.conn, "03-12-2024", "12:35", "Saddlemire")
        result: bool = insert_trail_user(self.conn, "03-12-2024", "12:35", "Saddlemire", 1)
        self.assertEqual(result, True)

    def test_insert_trail_user_again(self):
        result: bool = insert_trail_user(self.conn, "03-12-2024", "12:35", "Saddlemire", 1)
        self.assertEqual(result, False)