from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'', include('raid_scheduler.raid_calendar.urls')),
	(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'home/login.djhtml'} ),
	(r'^logout$', 'django.contrib.auth.views.logout' ),
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
)
