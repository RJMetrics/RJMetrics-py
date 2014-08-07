
import sys
import json

import requests


if sys.version < '3':
    _STR_TYPES = set([str, unicode])
    from itertools import izip_longest as zip_longest
else:
    _STR_TYPES = set([str])
    from itertools import zip_longest


def grouper(iterable, n, fillvalue=None):
    """
    Collect data into fixed-length chunks or blocks.

    grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx

    From: https://docs.python.org/2/library/itertools.html#recipes
    """
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


class Client(object):

    API_BASE = 'https://connect.rjmetrics.com/v2'
    SANDBOX_BASE = 'https://sandbox-connect.rjmetrics.com/v2'

    _AUTH_TEST_DATA = [{"keys": ["id"], "id": 1}]
    _MAX_RETRIES = 3
    _BATCH_SIZE = 100  # items per request

    def __init__(self, client_id, api_key):
        """
        Creates a new Python client to the RJMetrics API.
        """

        if type(client_id) != int:
            raise ValueError("Client ID '%s' must be an integer." % client_id)

        if type(api_key) not in _STR_TYPES:
            raise ValueError("Import API key '%s' must be a string." % api_key)

        self.client_id = client_id
        self.api_key = api_key

    @staticmethod
    def _url(base_url, client_id, table_name, api_key):

        return "%s/client/%s/table/%s/data?apikey=%s" % \
          (base_url, client_id, table_name, api_key)

    def authenticate(self):
        """
        Sends a test data point to the sandbox to check API_KEY credentials
        and returns True if the test data is accepted (False otherwise).
        """
        posts = self.push_data("test", self._AUTH_TEST_DATA, self.SANDBOX_BASE)
        return (posts[0].status_code == 201)

    def push_data(self, table_name, data, base_url=None):
        """
        Pushes data as a list of dicts to the Import API.

        Each data point should have a list of keys. For example:

        [{"keys": ["id"], "id": 1}]
        """
        if type(table_name) not in _STR_TYPES:
            raise ValueError("Table name '%s' must be a string." % table_name)

        if type(data) != list:
            raise ValueError("Data '%s' must be a list." % data)

        if len(data) == 0:
            return []

        if base_url is None:
            base_url = self.API_BASE

        url = Client._url(base_url, self.client_id, table_name, self.api_key)

        headers = {'Content-Type': 'application/json'}
        
        posts = []
        for batch in grouper(data, Client._BATCH_SIZE):
            batch = [x for x in batch if x != None]
            posts.append(requests.post(url, data=json.dumps(batch), headers=headers))

        return posts

    def stream_data():
        """
        Pushes data from an iterable.
        """
        raise NotImplementedError()

    def fetch_data():
        """
        Fetches a table from the Export API.
        """
        raise NotImplementedError()
