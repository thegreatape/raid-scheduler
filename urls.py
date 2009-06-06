from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^raid-scheduler/', include('raid_scheduler.raid_calendar.urls')),
	(r'^raid-scheduler/login$', 'django.contrib.auth.views.login', {'template_name': 'home/login.djhtml'} ),
	(r'^raid-scheduler/logout$', 'django.contrib.auth.views.logout' ),
	(r'^raid-scheduler/admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^raid-scheduler/admin/(.*)', admin.site.root),
)
