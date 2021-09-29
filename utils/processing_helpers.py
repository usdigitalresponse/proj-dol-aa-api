from typing import List
from database.db_connection import DatabaseConnection
from models.claim import Claim
from clients.notification.notification_client import NotificationClient, EmailArgs
import datetime
import random
from clients.form.jotform_client import JotformClient
from urllib.parse import urlencode
import os
import datetime
from utils.secrets import get_jotform_api_key
import json


def process_claim(
    db_connection: DatabaseConnection,
    claim: Claim,
    notificiation_client: NotificationClient,
    email_args: EmailArgs,
):
    # TODO: Generate form link for each claim.
    demo_form = random.randint(0, 2)
    params = dict()
    if demo_form == 0 or demo_form == 2:
        params["w1"] = "yes"
    if demo_form == 1 or demo_form == 2:
        params["w2"] = "yes"
    params["id"] = claim.id
    params["email"] = email_args.recipient_emails[0]
    params_str = urlencode(params)

    # TODO: Replace demo form with the complete form.
    form_id = os.getenv("JOTFORM_FORM_ID")
    claim.form_url = "https://form.jotform.com/{}?{}".format(form_id, params_str)
    email_args.html_content = "Hello,\nYou are receiving this email because we need more information from you about your benefits case.\nYou reported that you were not able or available to work for at least one week during which you were paid unemployment benefits.\nWe would like to verify that information. And, if you were indeed not able or available to work at some point, we would like to better understand why.\nPlease respond by September 30. Not responding by September 30 or responding untruthfully may negatively impact your benefits.\n<a href='{}'>Fill out the form</a>\nThank you,\nThe VT Department of Labor".format(
        claim.form_url
    )
    print(email_args.html_content)

    # Send email.
    claim.email_attempted_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    notificiation_client.send(email_args=email_args)

    # Update metadata in database.
    claim.updated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db_connection.update_row(claim)


def convert_form_responses_to_claims(submissions):
    claims = []
    for submission in submissions:
        id = None
        for a in submission["answers"].values():
            if a["name"] == "id" and "answer" in a:
                id = a["answer"]

        # TODO: Add exception for missing ID in form submission.
        if not id:
            continue

        # TODO: Do simple validation if we want to.
        claim = Claim(id=id)
        claim.response = json.dumps(submission)
        claim.response_received_at = submission["created_at"]
        claim.updated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        claims.append(claim)

    return claims
