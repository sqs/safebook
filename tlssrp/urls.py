from django.conf.urls.defaults import *

urlpatterns = patterns('safebook.tlssrp.views',
    (r'^register$', 'register'),
    (r'^edit/(?P<username>[\w\d]+)$', 'edit'),
)
