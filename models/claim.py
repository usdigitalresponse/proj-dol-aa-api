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
        self.created_at = None
        self.updated_at = None

    def to_sql_insert_statement(self, table_name):
        if (
            not self.form_url
            and not self.is_delivered_successfully
            and not self.email_attempted_at
            and not self.response_received_at
            and not self.response
            and not self.created_at
            and not self.updated_at
            and self.email
            and self.weeks
        ):
            created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            updated_at = created_at
            return "INSERT INTO {} (email, weeks, created_at, updated_at) VALUES ('{}', '{}', '{}', '{}')".format(
                table_name, self.email, self.weeks, created_at, updated_at
            )

        raise Exception("Cannot create SQL insert statement.")

    # def to_insert_values_statement(self):
    #     sql = "("
    #     if self.email:
    #         sql += "'{}', ".format(self.email)
    #     else:
    #         sql += "NULL, "

    #     if self.weeks:
    #         sql += "'{}', ".format(self.weeks)
    #     else:
    #         sql += "NULL, "

    #     if self.form_url:
    #         sql += "'{}', ".format(self.form_url)
    #     else:
    #         sql += "NULL, "

    #     if self.is_delivered_successfully:
    #         sql += "{}, ".format(self.is_delivered_successfully)
    #     else:
    #         sql += "NULL, "

    #     if self.email_attempted_at:
    #         sql += "'{}', ".format(self.email_attempted_at)
    #     else:
    #         sql += "NULL, "

    #     if self.response_received_at:
    #         sql += "'{}', ".format(self.response_received_at)
    #     else:
    #         sql += "NULL, "

    #     if self.response_received_at:
    #         sql += "'{}', ".format(self.response_received_at)
    #     else:
    #         sql += "NULL, "
    #     return "('{}', '{}')".format(self.email, self.weeks)

    def __repr__(self):
        return "Email: {}\n Weeks: {}\n".format(self.email, self.weeks)
