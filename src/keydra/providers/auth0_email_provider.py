from keydra.clients.auth0 import Auth0Client
from keydra.exceptions import ConfigException, RotationException
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
        
        print(self.auth0_client._token)
        
    def _distribute_email_credentials(self, secret, destination):
        self.auth0_client.update_email_provider(secret)
        return destination

    def rotate(self, secret):
        raise RotationException('Auth0 email provider does not support rotation')
    
    @exponential_backoff_retry(3)
    def distribute(self, secret, destination):
        return self._distribute_email_credentials(secret, destination)
        
        