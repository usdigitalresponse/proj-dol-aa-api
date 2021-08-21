from typing import List


class EmailArgs:
    def __init__(self, recipient_emails, subject, html_content):
        self.recipient_emails = recipient_emails
        self.subject = subject
        self.html_content = html_content


class NotificationClient:
    """Base class for notification operations."""

    def __init__(self, token: str, from_email: str):
        self.token = token
        self.from_email = from_email

    def _is_email_client(self):
        return False

    def _send_email(self, recipient_emails: List[str], subject: str, html_content: str):
        pass

    def send(
        self,
        email_args: EmailArgs = None,
    ):
        if self._is_email_client():
            self._send_email(
                email_args.recipient_emails, email_args.subject, email_args.html_content
            )
            return

        raise Exception("Invalid notification client.")
