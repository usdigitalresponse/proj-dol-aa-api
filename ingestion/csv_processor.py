import csv
import ingestion.validators as validators
import codecs
from database.db_connection import DatabaseConnection
from models.claim import Claim


class CSVProcessor:
    def __init__(self, use_db_connection=False):
        self.db_connection = None
        if use_db_connection:
            self.db_connection = DatabaseConnection(is_test=True)

    def ingest(self, filepath: str = "", body=None):
        """Ingest CSV, validate, and store into database.

        Expected CSV schema:

        email | bob@gmail.com | email address of claimant
        weeks | 2020-W01 2020-W10 | space separated year and ISO 8601 week date

        Takes in either a filepath or a body from s3 of type botocore.response.StreamingBody
        """
        if filepath:
            return self._ingest_from_filepath(filepath)
        if body:
            return self._ingest_from_s3(body)

        return False

    def _ingest_from_filepath(self, filepath: str):
        try:
            claims = []
            with open(filepath, newline="\n") as csvfile:
                reader = csv.reader(csvfile, delimiter=",")
                row_number = 1
                for row in reader:
                    email, weeks = row
                    if not validators.is_valid_email(email):
                        # TODO: process errors.
                        continue
                    if not validators.is_valid_weeks(weeks):
                        # TODO: process errors.
                        continue
                    row_number += 1
                    claims.append(Claim(email, weeks))
                print("Rows processed: " + str(row_number))

            if not self.db_connection:
                return

            for claim in claims:
                self.db_connection.write_row(claim)

        except:
            raise Exception("Error ingesting csv: {}".format(filepath))

    def _ingest_from_s3(self, body):
        try:
            claims = []
            row_number = 1
            for row in csv.DictReader(
                codecs.getreader("utf-8")(body), fieldnames=["email", "weeks"]
            ):
                email, weeks = row["email"], row["weeks"]
                if not validators.is_valid_email(email):
                    # TODO: process errors.
                    continue
                if not validators.is_valid_weeks(weeks):
                    # TODO: process errors.
                    continue
                row_number += 1
                claims.append(Claim(email, weeks))
            print("Rows processed: " + str(row_number))

            if not self.db_connection:
                return

            for claim in claims:
                self.db_connection.write_row(claim)

        except:
            raise Exception("Error ingesting csv")
