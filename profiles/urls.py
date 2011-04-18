from django.conf.urls.defaults import *

urlpatterns = patterns('safebook.profiles.views',
    (r'^$', 'index'),
    (r'^(?P<username>[\w\d]+)$', 'detail'),
)
