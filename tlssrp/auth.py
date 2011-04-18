import re

from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth.middleware import RemoteUserMiddleware

class SRPMiddleware(RemoteUserMiddleware):
    header = "SSL_SRP_USER"

class SRPBackend(RemoteUserBackend):
    supports_anonymous_user = False
    
    clean_username_re = re.compile(r'[^a-zA-Z0-9]')

    def clean_username(self, username):
        """
        Strip out anything that could confuse the SRP passwd parser.
        TODO(sqs): this is way too strict.
        """
        return self.clean_username_re.sub('', username)
