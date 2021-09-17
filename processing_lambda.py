"""
This lambda function will trigger daily.

It will pull the latest x entries from the database that have not yet been processed.
It will generate form links for each of these entries, send out the forms in an email, and update the relevant metadata in the database.
"""
from ingestion.csv_processor import CSVProcessor
import urllib.parse
import json
from database.db_connection import DatabaseConnection


def lambda_handler(event, context):
    try:
        db_connection = DatabaseConnection(is_test=False)

        num_entries = 0
        db_connection.fetch_unprocessed_rows()

        db_connection.close()

        return {
            "statusCode": 200,
            "body": json.dumps("Success. Processed {} entries.".format(num_entries)),
        }
    except Exception as e:
        print(e)
        raise e
