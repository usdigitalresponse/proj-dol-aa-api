import datetime


class Claim:
    def __init__(self, email, weeks):
        self.email = email
        self.weeks = weeks
        self.form_url = None
        self.is_delivered_successfully = None
        self.email_attempted_at = None
        self.response_received_at = None
        self.response = None
        self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = self.created_at

    def to_sql_insert_statement(self, table_name):
        if self.email and self.weeks:
            return "INSERT INTO {} (email, weeks, created_at, updated_at) VALUES ('{}', '{}', '{}', '{}')".format(
                table_name, self.email, self.weeks, self.created_at, self.updated_at
            )

        raise Exception("Cannot create SQL insert statement.")

    def to_sql_update_statement(self, table_name):
        set_statement = ""

        if self.form_url:
            set_statement += "form_url='{}', ".format(self.form_url)

        if self.is_delivered_successfully:
            set_statement += "is_delivered_successfully={}, ".format(
                self.is_delivered_successfully
            )

        if self.email_attempted_at:
            set_statement += "email_attempted_at='{}', ".format(self.email_attempted_at)

        if self.response_received_at:
            set_statement += "response_received_at='{}', ".format(
                self.response_received_at
            )

        if self.response:
            set_statement += "response='{}', ".format(self.response)

        if self.updated_at:
            set_statement += "updated_at='{}', ".format(self.updated_at)

        if set_statement:
            # Remove extra space and comma at the end.
            set_statement = set_statement[:-2]
        else:
            # This is a no-op update.
            return None

        return "UPDATE {} SET {} WHERE email='{}'".format(
            table_name, set_statement, self.email
        )

    def __repr__(self):
        return "Email: {}\n Weeks: {}\n".format(self.email, self.weeks)


def unpacking_func(row):
    """
    Unpack a MySQL row (dictionary with keys as col names) into a claim object.
    """
    claim = Claim(row["email"], row["weeks"])

    claim.form_url = row["form_url"]
    claim.is_delivered_successfully = row["is_delivered_successfully"]
    claim.email_attempted_at = row["email_attempted_at"]
    claim.response_received_at = row["response_received_at"]
    claim.response = row["response"]
    claim.created_at = row["created_at"]
    claim.updated_at = row["updated_at"]
    return claim
