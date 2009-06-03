from django.conf.urls.defaults import *

urlpatterns = patterns('raid_scheduler.raid_calendar.views',
	(r'^$', 'home'),
	(r'^signup$', 'create_user'),
	(r'^logout$', 'logout_user' ),
	(r'^(?P<raid_id>\d+)$', 'view_raid')
)
