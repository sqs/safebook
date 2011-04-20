import os
import sys

path = '/home/sqs/src/'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'safebook.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

