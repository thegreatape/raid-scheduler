from raid_scheduler.raid_calendar.models import Raid
from django.contrib import admin

class RaidAdmin(admin.ModelAdmin):
	fields = ('title', 'date', 'roll_date', 'raid_leader')
						
admin.site.register(Raid, RaidAdmin)
