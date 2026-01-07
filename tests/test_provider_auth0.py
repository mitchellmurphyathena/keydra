import unittest
from unittest.mock import MagicMock, patch

from keydra.exceptions import ConfigException, DistributionException
from keydra.providers.auth0 import Client

VALID_CREDENTIALS = {
    'clientId': 'test_client_id',
    'clientSecret': 'test_client_secret',
    'domain': 'test_domain',
    'audience': 'test_audience'
}

SECRET = VALID_CREDENTIALS

class TestProviderAuth0(unittest.TestCase):

    @patch('keydra.providers.auth0.Auth0Client')
    def test__init_with_credentials(self, mock_auth0_client):
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

    @patch('keydra.providers.auth0.Auth0Client')
    def test__rotate_client_secret(self, mock_auth0_client):
        mock_client_instance = MagicMock()
        mock_client_instance.post_rotate_client.return_value = 'new_secret_value'
        mock_auth0_client.return_value = mock_client_instance

        client = Client(credentials=VALID_CREDENTIALS)
        result = client._rotate_client_secret()

        self.assertEqual(result['clientId'], 'test_client_id')
        self.assertEqual(result['clientSecret'], 'new_secret_value')
        self.assertEqual(result['domain'], 'test_domain')
        self.assertEqual(result['audience'], 'test_audience')
        mock_client_instance.post_rotate_client.assert_called_once()

    @patch('keydra.providers.auth0.Auth0Client')
    def test__rotate(self, mock_auth0_client):
        mock_client_instance = MagicMock()
        mock_client_instance.post_rotate_client.return_value = 'rotated_secret'
        mock_auth0_client.return_value = mock_client_instance

        client = Client(credentials=VALID_CREDENTIALS)
        result = client.rotate({})

        self.assertEqual(result['clientSecret'], 'rotated_secret')
        mock_client_instance.post_rotate_client.assert_called_once()
