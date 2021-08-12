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
            with open(filepath, newline='\n') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                row_number = 1
                for row in reader:
                    email, weeks = row
                    if not validators.is_valid_email(email):
                        raise Exception("Invalid email {} in row {}".format(email, row_number))
                    if not validators.is_valid_weeks(weeks):
                        raise Exception("Invalid weeks {} in row {}".format(weeks, row_number))
        except:
            raise Exception("Error ingesting csv: {}".format(filepath))
