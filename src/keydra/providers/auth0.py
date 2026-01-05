from keydra.clients.aws.secretsmanager import SecretsManagerClient
from keydra.clients.auth0 import Auth0Client
from keydra.exceptions import ConfigException, DistributionException
from keydra.providers.base import BaseProvider, exponential_backoff_retry

class Client(BaseProvider):
    def __init__(self, session=None, credentials: dict = None, region_name=None):
        if not credentials:
            raise ConfigException(
                'Credentials are required for Auth0 provider')

        self._orig_secret = credentials
        
        self.auth0_client = Auth0Client(
            client_id=credentials.get('clientId'),
            client_secret=credentials.get('clientSecret'),
            domain=credentials.get('domain'),
            audience=credentials.get('audience')
        )
        
    def _rotate_client_secret(self, secret):
        new_client_secret = self.auth0_client.post_rotate_client()
        
        return {
            **self._orig_secret,
            'clientSecret': new_client_secret,
        }
        
    @exponential_backoff_retry(3)
    def rotate(self, secret):
        return self._rotate_client_secret(secret)
    
    def distribute(self, secret, destination):
        raise DistributionException('Auth0 does not support distribution')