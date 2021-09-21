import pymysql
import os

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
                cursorclass=pymysql.cursors.DictCursor,
            )
        except pymysql.MySQLError as e:
            print("ERROR: Unexpected error: Could not connect to MySQL instance.")

    def write_row(self, model):
        with self.conn.cursor() as cur:
            sql_statement = model.to_sql_insert_statement(table_name)
            cur.execute(sql_statement)
        self.conn.commit()
        cur.close()

    def update_row(self, model):
        with self.conn.cursor() as cur:
            update_statement = model.to_sql_update_statement(table_name)
            if update_statement:
                cur.execute(update_statement)
        self.conn.commit()
        cur.close()

    def fetch_all_rows(self, unpacking_func):
        res = []
        cur = self.conn.cursor()
        cur.execute("SELECT * from {}".format(table_name))
        rows = cur.fetchall()
        for row in rows:
            res.append(unpacking_func(row))
        return res

    def fetch_unprocessed_rows(self, unpacking_func, limit=10000):
        res = []
        cur = self.conn.cursor()
        cur.execute(
            "SELECT * FROM {} WHERE email_attempted_at IS NULL ORDER BY created_at ASC LIMIT {}".format(
                table_name, limit
            )
        )
        rows = cur.fetchall()
        for row in rows:
            res.append(unpacking_func(row))
        return res

    def clear_table(self):
        with self.conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE {}".format(table_name))
        self.conn.commit()
        cur.close()

    def reset_table(self):
        with self.conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS claims")
            cur.execute(
                """
                CREATE TABLE claims (
                    id VARCHAR(36) NOT NULL,
                    email VARCHAR(256) NOT NULL,
                    weeks VARCHAR(1024) NOT NULL,

                    form_url VARCHAR(256),
                    is_delivered_successfully TINYINT(1),
                    email_attempted_at DATETIME(6),
                    response_received_at DATETIME(6),
                    response BLOB,

                    created_at DATETIME(6),
                    updated_at DATETIME(6),

                    PRIMARY KEY (id)
                )
                """
            )
        self.conn.commit()
        cur.close()

    def close(self):
        self.conn.close()
