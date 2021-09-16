import re

email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


def is_valid_email(email: str):
    if re.fullmatch(email_regex, email):
        return True
    return False


def is_valid_weeks(weeks):
    return True
