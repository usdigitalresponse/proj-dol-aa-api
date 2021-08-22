import csv
import validators


class CSVProcessor:
    def __init__(self):
        pass

    def ingest(self, filepath: str):
        """Ingest CSV, validate, and store into database.

        Expected CSV schema:

        email | bob@gmail.com | email address of claimant
        weeks | 2020-W01 2020-W10 | space separated year and ISO 8601 week date
        """
        try:
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

                # TODO: insert row into database.

        except:
            raise Exception("Error ingesting csv: {}".format(filepath))
