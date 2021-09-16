from clients.notification.sendgrid_client import SendGridClient
from clients.notification.notification_client import EmailArgs
from clients.form.jotform_client import JotformClient
import os
from ingestion.csv_processor import CSVProcessor
from database.db_connection import DatabaseConnection
from models.claim import Claim


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


def test_jotform_client():
    token = os.getenv("JOTFORM_API_KEY")
    jotform_client = JotformClient(token)


def test_notification_client():
    pass


def test_ingestion():
    """
    Ingest rows from a CSV file into test database.
    """
    db_connection = DatabaseConnection()
    db_connection.clear_table()

    csv_processor = CSVProcessor(db_connection)
    csv_processor.ingest(filepath="test_claims.csv")

    rows = db_connection.fetch_all_rows(lambda row: Claim(row["email"], ""))
    assert len(rows) == 3

    db_connection.clear_table()
    db_connection.close()


if __name__ == "__main__":
    test_ingestion()
