from clients.notification.notification_client import NotificationClient
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from typing import List


class SendGridClient(NotificationClient):
    def __init__(self, token: str, from_email: str):
        super().__init__(token, from_email)
        self.client = SendGridAPIClient(self.token)

    def _is_email_client(self):
        return True

    def _send_email(self, recipient_emails: List[str], subject: str, html_content: str):
        message = Mail(
            from_email=self.from_email,
            to_emails=recipient_emails,
            subject=subject,
            html_content=html_content,
        )

        try:
            resp = self.client.send(message)
            print(resp.status_code)
        except Exception as e:
            print(e.message)
