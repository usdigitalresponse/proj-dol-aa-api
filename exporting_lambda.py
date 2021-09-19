"""
This lambda function will trigger daily.

It will pull all the form results from the last day via. form API.
It will update the metadata on these rows of the database.
"""
from ingestion.csv_processor import CSVProcessor
import json
from database.db_connection import DatabaseConnection
from clients.form.form_client import FormClient
from utils.processing_helpers import convert_form_responses_to_claims


def lambda_handler(event, context):
    try:
        db_connection = DatabaseConnection(is_test=False)
        num_entries = 0

        # TODO: Call Form API to collect repsonses.
        # token = "<token>"
        # form_client = FormClient(token)
        # form_client.get_response(timedelta=24)
        claims = convert_form_responses_to_claims()

        for claim in claims:
            db_connection.update_row(claim)

        # TODO: Export entire database as CSV and email to recipient.

        db_connection.close()

        return {
            "statusCode": 200,
            "body": json.dumps("Success. Processed {} entries.".format(num_entries)),
        }
    except Exception as e:
        print(e)
        raise e
