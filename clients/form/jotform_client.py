from jotform import *
import os

class JotformClient:
    """
    Jotform client to interact with the API client
    """
    def __init__(self, token):
        self.client = JotformAPIClient(token)
        self.form_id = os.getenv("JOTFORM_FORM_ID")
    
    def fetch_responses(self, day):
        '''
        day is in format yyyy-mm-dd
        i.e. day = "2020-09-19"
        '''
        limit = 1000
        offset = 0
        orderby = "created_at"
        filter = {"created_at:gt":"{} 00:00:00".format(day), "created_at:lt": "{} 23:59:59".format(day)}

        submissions = []
        while True:
            sub_chunk = self.client.get_form_submissions(self.form_id, offset, limit, filter, orderby)
            submissions += sub_chunk
            if len(submissions) < limit:
                break
            offset += limit
        return submissions

