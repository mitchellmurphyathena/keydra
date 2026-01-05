import unittest
from unittest.mock import MagicMock, patch

from keydra.clients.auth0 import Auth0Client


class TestAuth0Client(unittest.TestCase):

    @patch('keydra.clients.auth0.GetToken')
    @patch('keydra.clients.auth0.Clients')
    def test__init(self, mock_clients, mock_get_token):
        mock_token_instance = MagicMock()
        mock_token_instance.client_credentials.return_value = {'access_token': 'test_token'}
        mock_get_token.return_value = mock_token_instance

        client = Auth0Client(
            client_id='test_client_id',
            client_secret='test_client_secret',
            domain='test_domain',
            audience='test_audience'
        )

        self.assertEqual(client._token, 'test_token')
        self.assertEqual(client._client_id, 'test_client_id')
        self.assertEqual(client._domain, 'test_domain')
        self.assertEqual(client._audience, 'test_audience')

        mock_get_token.assert_called_once_with('test_domain', 'test_client_id', 'test_client_secret')
        mock_token_instance.client_credentials.assert_called_once_with('test_audience')

    @patch('keydra.clients.auth0.GetToken')
    @patch('keydra.clients.auth0.Clients')
    def test__post_rotate_client(self, mock_clients_class, mock_get_token):
        mock_token_instance = MagicMock()
        mock_token_instance.client_credentials.return_value = {'access_token': 'test_token'}
        mock_get_token.return_value = mock_token_instance

        mock_clients_instance = MagicMock()
        mock_clients_instance.rotate_secret.return_value = {'client_secret': 'new_secret'}
        mock_clients_class.return_value = mock_clients_instance

        client = Auth0Client(
            client_id='test_client_id',
            client_secret='test_client_secret',
            domain='test_domain',
            audience='test_audience'
        )

        new_secret = client.post_rotate_client()

        self.assertEqual(new_secret, 'new_secret')
        mock_clients_class.assert_called_with('test_domain', 'test_token')
        mock_clients_instance.rotate_secret.assert_called_once_with('test_client_id')
