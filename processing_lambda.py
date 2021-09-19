"""
This lambda function will trigger daily.

It will pull the latest x entries from the database that have not yet been processed.
It will generate form links for each of these entries, send out the forms in an email, and update the relevant metadata in the database.
"""
import json
import os
from database.db_connection import DatabaseConnection
from utils.processing_helpers import process_claim
from clients.notification.sendgrid_client import SendGridClient
from clients.notification.notification_client import EmailArgs
from models.claim import unpacking_func


def lambda_handler(event, context):
    try:
        db_connection = DatabaseConnection(is_test=False)

        # Setup SendGrid client.
        token = os.getenv("SENDGRID_API_KEY")
        from_email = "ui-fact-finding@usdigitalresponse.org"
        sendgrid_client = SendGridClient(token, from_email)

        num_entries = 0
        unprocessed_claims = db_connection.fetch_unprocessed_rows(unpacking_func)

        for claim in unprocessed_claims:
            email_args = EmailArgs(
                [claim.email],
                "[Department of Labor] Fill out UI Form",
                "",
            )
            process_claim(db_connection, claim, sendgrid_client, email_args)
            num_entries = +1

        db_connection.close()

        return {
            "statusCode": 200,
            "body": json.dumps("Success. Processed {} entries.".format(num_entries)),
        }
    except Exception as e:
        print(e)
        raise e
