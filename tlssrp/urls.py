from django.conf.urls.defaults import *

urlpatterns = patterns('safebook.tlssrp.views',
    (r'^register$', 'register'),
)
