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


def process_claim(
    db_connection: DatabaseConnection,
    claim: Claim,
    notificiation_client: NotificationClient,
    email_args: EmailArgs,
):
    # TODO: Generate form link for each claim.
    demo_form = random.randint(0, 2)
    params = dict()
    if demo_form == 0 or demo_form == 2: params['week1'] = 'yes'
    if demo_form == 1 or demo_form == 2: params['week2'] = 'yes'
    params['id'] = claim.id
    params_str = urlencode(params)
    
    # TODO: Replace demo form with the complete form.
    form_id = os.getenv("JOTFORM_FORM_ID")
    claim.form_url = "https://form.jotform.com/{}".format(form_id)
    email_args.html_content = "Please fill out this form: {}?{}".format(claim.form_url, params_str)
    print (email_args.html_content)

    # Send email.
    claim.email_attempted_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    notificiation_client.send(email_args=email_args)

    # Update metadata in database.
    claim.updated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db_connection.update_row(claim)


def convert_form_responses_to_claims():
    token = get_jotform_api_key()
    jotform_client = JotformClient(token)
    today = datetime.today().strftime('%Y-%m-%d')
    submissions = jotform_client.fetch_responses(today)

    claims = []
    for submission in submissions:
        id = [a for a in submission['answers'] if a['name'] == 'id']
        
        # TODO: Do simple validation if we want to.
        claim = Claim(id=id)
        claim.response = submission
        claim.response_received_at = submission['created_at']
        claim.updated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        claims.append(claim)

    return claims
