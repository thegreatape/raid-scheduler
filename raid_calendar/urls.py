from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse

urlpatterns = patterns('raid_scheduler.raid_calendar.views',
	url(r'^$', 'home', name="home"),
	url(r'^signup$', 'create_user', name="create_user"),
	url(r'^logout$', 'logout_user', name="logout_user"),
	url('^(?P<raid_id>\d+)$', 'view_raid', name="view_raid")
)
