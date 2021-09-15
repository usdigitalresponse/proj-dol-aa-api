from jotform import *

class JotformClient:
    """
    Jotform client to interact with the API client
    """
    def __init__(self, token):
        self.client = JotformAPIClient(token)
    


