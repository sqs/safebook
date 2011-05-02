import re

from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth.middleware import RemoteUserMiddleware

class SRPMiddleware(RemoteUserMiddleware):
    header = "SSL_SRP_USER"

class SRPBackend(RemoteUserBackend):
    supports_anonymous_user = False
