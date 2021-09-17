from typing import List
from database.db_connection import DatabaseConnection
from models.claim import Claim
from clients.notification.notification_client import NotificationClient, EmailArgs
import datetime


def process_claim(
    db_connection: DatabaseConnection,
    claim: Claim,
    notificiation_client: NotificationClient,
    email_args: EmailArgs,
):
    # TODO: Generate form link for each claim.
    claim.form_url = "dummy.url/form"
    email_args.html_content = "Please fill out this form: {}".format(claim.form_url)

    # Send email.
    claim.email_attempted_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    notificiation_client.send(email_args=email_args)

    # Update metadata in database.
    claim.updated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db_connection.update_row(claim)
