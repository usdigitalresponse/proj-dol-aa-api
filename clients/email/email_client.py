class EmailClient:
    """Base class for email operations.
    """
    def __init__(self, token):
        self.token = token
