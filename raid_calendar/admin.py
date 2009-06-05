from raid_scheduler.raid_calendar.models import Raid, Registration
from django.contrib import admin

class RegistrationInline(admin.TabularInline):
	model = Registration
	extra = 1

class RaidAdmin(admin.ModelAdmin):
	fields = ('title', 'description', 'date', 'roll_date', 'dps_spots', 'tank_spots', 'healer_spots')
	inlines = (RegistrationInline,)
	list_display = ('title', 'date')
	
admin.site.register(Raid, RaidAdmin)
