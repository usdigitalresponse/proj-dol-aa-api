import pymysql
import os
from models.claim import Claim

rds_host = os.getenv("RDS_HOST")
name = os.getenv("RDS_USERNAME")
password = os.getenv("RDS_PASSWORD")
db_name = os.getenv("DB_NAME")
table_name = "claims"


class DatabaseConnection:
    def __init__(self, is_test=True):
        try:
            self.conn = pymysql.connect(
                host=rds_host,
                user=name,
                passwd=password,
                db=db_name + "_test" if is_test else db_name,
                connect_timeout=5,
            )
        except pymysql.MySQLError as e:
            print("ERROR: Unexpected error: Could not connect to MySQL instance.")

    def write_row(self, row: Claim):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO {} VALUES ({}, {})".format(
                    table_name, row.email, row.weeks
                )
            )
        self.conn.commit()

    def print_all_rows(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * from {}".format(table_name))
            for row in cur:
                print(row)

    def clear_table(self):
        with self.conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE {}".format(table_name))
        self.conn.commit()
