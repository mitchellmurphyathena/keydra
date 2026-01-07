import unittest
from unittest.mock import MagicMock, patch

from keydra.exceptions import ConfigException, RotationException
from keydra.providers.auth0_email_provider import Client


VALID_CREDENTIALS = {
    'clientId': 'test_client_id',
    'clientSecret': 'test_client_secret',
    'domain': 'test_domain',
    'audience': 'test_audience'
}


class TestProviderAuth0EmailProvider(unittest.TestCase):

    @patch('keydra.providers.auth0_email_provider.Auth0Client')
    def test__init_with_credentials(self, mock_auth0_client):
        mock_client_instance = MagicMock()
        mock_client_instance._token = 'test_token'
        mock_auth0_client.return_value = mock_client_instance

        client = Client(credentials=VALID_CREDENTIALS)

        self.assertEqual(client._orig_secret, VALID_CREDENTIALS)
        mock_auth0_client.assert_called_once_with(
            client_id='test_client_id',
            client_secret='test_client_secret',
            domain='test_domain',
            audience='test_audience'
        )

    def test__init_without_credentials(self):
        with self.assertRaises(ConfigException) as context:
            Client()

        self.assertEqual(str(context.exception), 'Credentials are required for Auth0 provider')

    @patch('keydra.providers.auth0_email_provider.Auth0Client')
    def test__distribute_email_credentials(self, mock_auth0_client):
        mock_client_instance = MagicMock()
        mock_client_instance._token = 'test_token'
        mock_auth0_client.return_value = mock_client_instance

        client = Client(credentials=VALID_CREDENTIALS)

        secret = {
            'api_key': 'test_api_key',
            'api_secret': 'test_api_secret',
            'smtp_host': 'smtp.example.com'
        }

        destination = {
            'source': {
                'name': 'api_key',
                'api_key': 'api_key',
                'api_user': 'api_secret'
            }
        }

        result = client._distribute_email_credentials(secret, destination)

        expected_post_data = {
            'name': 'test_api_key',
            'api_key': 'test_api_key',
            'api_user': 'test_api_secret'
        }

        self.assertEqual(result, destination)
        mock_client_instance.update_email_provider.assert_called_once_with(expected_post_data)

    @patch('keydra.providers.auth0_email_provider.Auth0Client')
    def test__distribute(self, mock_auth0_client):
        mock_client_instance = MagicMock()
        mock_client_instance._token = 'test_token'
        mock_auth0_client.return_value = mock_client_instance

        client = Client(credentials=VALID_CREDENTIALS)

        secret = {
            'username': 'test_user',
            'password': 'test_pass'
        }

        destination = {
            'source': {
                'accessKeyId': 'username',
                'secretAccessKey': 'password'
            }
        }

        result = client.distribute(secret, destination)

        expected_post_data = {
            'accessKeyId': 'test_user',
            'secretAccessKey': 'test_pass'
        }

        self.assertEqual(result, destination)
        mock_client_instance.update_email_provider.assert_called_once_with(expected_post_data)
