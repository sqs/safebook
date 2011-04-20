from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^auth/', include('safebook.tlssrp.urls')),
    (r'', include('safebook.profiles.urls')),
)
