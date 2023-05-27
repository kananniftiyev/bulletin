from django.test import TestCase
from django.db import connection


class DatabaseConnectionTest(TestCase):
    def test_database_connection(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(result)  # Add this line to print the result

        self.assertEqual(result, (1,))