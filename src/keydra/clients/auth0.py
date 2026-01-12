from auth0.authentication import GetToken
from auth0.management import Emails, Clients

class Auth0Client(object):
    def __init__(self, client_id=None, client_secret=None, domain=None, audience=None):
        token = GetToken(domain, client_id, client_secret).client_credentials(audience)
        
        self._token = token['access_token']
        self._client_id = client_id
        self._domain = domain
        self._audience = audience
        
    def post_rotate_client(self):
        new_client_secret = Clients(self._domain, self._token).rotate_secret(self._client_id)['client_secret']
        
        return new_client_secret
    
    def update_email_provider(self, email_provider_credentials):
        Emails(self._domain, self._token).update({
            "credentials": email_provider_credentials,
        })
