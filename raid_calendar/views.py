from django.http import HttpResponse
from django.shortcuts import render_to_response
from calendar import Calendar

from datetime import date, datetime
from raid_calendar.models import Raid

def home(request):
	today = date.today()
	raids = Raid.objects.filter(date__gte=datetime(today.year, today.month, 1))
	days = sum(Calendar().monthdayscalendar(today.year, today.month), [])
	for raid in raids:
		days[days.index(raid.date.day)] = "%i - %s" % (raid.date.day, raid.title)
	context = {'date': today.strftime('%B %Y'),
			   'days' : days}
	return render_to_response('home/calendar.djhtml', context)
