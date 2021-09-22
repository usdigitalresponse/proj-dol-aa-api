from clients.notification.sendgrid_client import SendGridClient
from clients.notification.notification_client import EmailArgs
from clients.form.jotform_client import JotformClient
import os
from ingestion.csv_processor import CSVProcessor
from database.db_connection import DatabaseConnection
from models.claim import unpacking_func, Claim
from utils.processing_helpers import process_claim, convert_form_responses_to_claims
from datetime import datetime
from utils.exporting_helpers import claims_to_csv


def test_end_to_end():
    """
    Reads CSV.
    Parses and stores claims into database.
    Generates forms URLs.
    Sends out emails with forms.
    [Fills in sample response(s)]
    Pulls form responses.
    Generates CSV export.
    """
    pass


def test_sengrid_client():
    """
    ** Make sure to run source ./sendgrid.env before running this test **

    Test sending an email using the SendGrid client.
    """
    token = os.getenv("SENDGRID_API_KEY")
    from_email = "ui-fact-finding@usdigitalresponse.org"
    sendgrid_client = SendGridClient(token, from_email)

    # Valid recipients.
    recipient_emails = ["ui-fact-finding@usdigitalresponse.org"]
    subject = "Unemployment Able & Available [TEST]"
    html_content = "<strong> Please fill out this form: www.form.com/form </strong>"

    email_args = EmailArgs(recipient_emails, subject, html_content)
    sendgrid_client.send(email_args=email_args)


def test_notification_client():
    pass


def test_ingestion():
    """
    Ingest rows from a CSV file into test database.
    """
    db_connection = DatabaseConnection()
    db_connection.clear_table()

    csv_processor = CSVProcessor(db_connection)
    csv_processor.ingest(filepath="test_claims_real.csv")

    rows = db_connection.fetch_all_rows(unpacking_func)
    assert len(rows) == 2

    db_connection.clear_table()
    db_connection.close()


def test_processing():
    """
    Test pulling for unprocessed rows and processing them.
    """
    db_connection = DatabaseConnection()
    db_connection.clear_table()

    # Setup SendGrid client.
    token = os.getenv("SENDGRID_API_KEY")
    from_email = "ui-fact-finding@usdigitalresponse.org"
    sendgrid_client = SendGridClient(token, from_email)

    # Seed database with fake rows.
    csv_processor = CSVProcessor(db_connection)
    csv_processor.ingest(filepath="tests/test_claims_real.csv")

    # Fetch unprocessed rows.
    claims = db_connection.fetch_unprocessed_rows(unpacking_func)
    assert len(claims) == 2

    # Process rows.
    for claim in claims:
        email_args = EmailArgs(
            [claim.email],
            "[TEST] Fill out UI Form",
            "",
        )
        process_claim(db_connection, claim, sendgrid_client, email_args)

    db_connection.clear_table()
    db_connection.close()


def test_pulling_form_responses():
    """
    Test pulling Jotform repsonses and writing them to appropriate row in database.
    """
    db_connection = DatabaseConnection()
    db_connection.clear_table()

    test_claim = Claim(id="1234", email="advith.chelikani@gmail.com", weeks="W01")
    db_connection.write_row(test_claim)

    token = os.getenv("JOTFORM_API_KEY")
    jotform_client = JotformClient(token)
    submissions = jotform_client.fetch_responses("2021-09-21")fe

    claims = convert_form_responses_to_claims(submissions)

    for claim in claims:
        db_connection.update_row(claim)

    # db_connection.clear_table()
    db_connection.close()


def test_exporting_to_csv():
    """
    Test exporting all database records into CSV.
    """
    db_connection = DatabaseConnection()
    db_connection.clear_table()

    # Seed database with fake rows.
    csv_processor = CSVProcessor(db_connection)
    csv_processor.ingest(filepath="tests/test_claims_real.csv")

    # Fetch all claims.
    claims = db_connection.fetch_all_rows(unpacking_func)

    # Turn into CSV.
    claims_to_csv(claims, "test_export.csv")

    db_connection.clear_table()
    db_connection.close()


if __name__ == "__main__":
    test_pulling_form_responses()
