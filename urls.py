from django.conf.urls.defaults import *
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'', include('raid_scheduler.raid_calendar.urls')),
    (r'^login$', 'django.contrib.auth.views.login', {'template_name': 'home/login.djhtml'} ),
    (r'^logout$', 'django.contrib.auth.views.logout' ),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^reset-password$', password_reset, {'email_template_name': 'home/reset_password_email.djhtml'}),
    (r'^reset-password/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm),
    (r'^reset-password-done$', password_reset_done),
    (r'^reset-password-confirm$', password_reset_confirm),
    (r'^password-reset-complete$', password_reset_complete),
    (r'^admin/(.*)', admin.site.root),
)
