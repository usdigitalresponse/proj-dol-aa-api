class Claim:
    def __init__(self, email, weeks):
        self.email = email
        self.weeks = weeks

    def to_insert_values_statement(self):
        return "('{}')".format(self.email)

    def __repr__(self):
        return "Email: {}\n Weeks: {}\n".format(self.email, self.weeks)
