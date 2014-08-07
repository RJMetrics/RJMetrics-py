
import itertools
import json
import sys
import unittest

import mock

from rjmetrics.client import Client


API_KEY = 'test-api-key'
CLIENT_ID = 12
JSON_HEADER = {'Content-Type': 'application/json'}


class TestClientInit(unittest.TestCase):

    def test_init_success(self):
        test_client = Client(CLIENT_ID, API_KEY)
        self.assertTrue(isinstance(test_client, Client))

        if sys.version < '3':
            test_client = Client(CLIENT_ID, unicode(API_KEY))
            self.assertTrue(isinstance(test_client, Client))

    def test_init_requires_int_client_id(self):
        self.assertRaises(ValueError, Client, str(CLIENT_ID), API_KEY)

    def test_init_requires_str_or_unicode_api_key(self):
        self.assertRaises(ValueError, Client, CLIENT_ID, 30)


class TestClient(unittest.TestCase):

    def setUp(self):
        self.client = Client(CLIENT_ID, API_KEY)

    ## authenticate

    @mock.patch('requests.post')
    def test_authenticate_succeeds_on_test_data_created(self, mock_post):
        mock_post.return_value.status_code = 201

        self.assertTrue(self.client.authenticate())

        mock_post.assert_called_once_with(
            'https://sandbox-connect.rjmetrics.com/v2/'
            'client/12/table/test/data?apikey=test-api-key',
            data=json.dumps(Client._AUTH_TEST_DATA),
            headers=JSON_HEADER)

    @mock.patch('requests.post')
    def test_authenticate_fails_on_unauthorized(self, mock_post):
        mock_post.return_value.status_code = 401

        self.assertFalse(self.client.authenticate())

        mock_post.assert_called_once_with(
            'https://sandbox-connect.rjmetrics.com/v2/'
            'client/12/table/test/data?apikey=test-api-key',
            data=json.dumps(Client._AUTH_TEST_DATA),
            headers=JSON_HEADER)


    ## push_data

    def test_push_data_requires_str_or_unicode_tablename(self):
        self.assertRaises(ValueError, self.client.push_data, 20, []);

    def test_push_data_requires_list_data(self):
        self.assertRaises(ValueError, self.client.push_data, '20', set());

    def test_push_data_no_data_returns_empty_list(self):
        self.assertEqual(self.client.push_data('20', []), []);

    @mock.patch('requests.post')
    def test_push_data_one_batch(self, mock_post):
        test_data = list(itertools.repeat(Client._AUTH_TEST_DATA[0], 2))

        mock_post.return_value.status_code = 201

        self.client.push_data('test', test_data, Client.SANDBOX_BASE)

        mock_post.assert_called_once_with(
            'https://sandbox-connect.rjmetrics.com/v2/'
            'client/12/table/test/data?apikey=test-api-key',
            data=json.dumps(test_data),
            headers=JSON_HEADER)

    @mock.patch('requests.post')
    def test_push_data_many_batches(self, mock_post):
        # breaks data into BATCH_SIZE batches
        test_data = [{"keys": ["id"], "id": i} for i in range(144)]

        mock_post.return_value.status_code = 201

        self.client.push_data('test', test_data, Client.SANDBOX_BASE)

        expected_url = 'https://sandbox-connect.rjmetrics.com/v2/' \
            'client/12/table/test/data?apikey=test-api-key'

        self.assertEqual(mock_post.call_args_list[0],
                         mock.call(expected_url,
                                   data=json.dumps(test_data[0:Client._BATCH_SIZE]),
                                   headers=JSON_HEADER))

        self.assertEqual(mock_post.call_args_list[1],
                         mock.call(expected_url,
                                   data=json.dumps(test_data[Client._BATCH_SIZE:]),
                                   headers=JSON_HEADER))
