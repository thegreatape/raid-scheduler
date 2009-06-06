from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.urlresolvers import reverse

from calendar import Calendar
from forms import RegistrationForm
from datetime import date, datetime
from raid_calendar.models import Raid, Registration

def home(request):
	today = date.today()
	raids = Raid.objects.filter(date__gte=datetime(today.year, today.month, 1))
	days = [{'day': x} for x in sum(Calendar().monthdayscalendar(today.year, today.month), [])]

	for raid in raids:
		event = days[days.index({'day': raid.date.day})]
		if "raids" in event:
			event["raids"].append(raid)
		else:
			event["raids"] = [raid]

	context = {'date': today.strftime('%B %Y'),
			   'days' : days}
	return render_to_response('home/calendar.djhtml', context, context_instance=RequestContext(request))

@login_required
def view_raid(request, raid_id):
	raid = get_object_or_404(Raid, id=raid_id)
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			registration = Registration(player=request.user,
										raid=raid,
										role=form.cleaned_data['role'])
			if 'standby' in cleaned_data:
				registration.standby = form.cleaned_date['standby'] 
			registration.save()
	else:
		form = RegistrationForm()

	dps = Registration.objects.filter(raid=raid,role="dps").order_by("number")
	tanks = Registration.objects.filter(raid=raid,role="tank").order_by("number")
	healers = Registration.objects.filter(raid=raid,role="healer").order_by("number")

	if raid.has_rolled:
		registered = {
			'DPS': (('guaranteed', dps[:raid.dps_spots]), ('standby', dps[raid.dps_spots:])),
			'Tanks': (('guaranteed', tanks[:raid.tank_spots]), ('standby', tanks[raid.tank_spots:])),
			'Healers': (('guaranteed', healers[:raid.healer_spots]), ('standby', healers[raid.healer_spots:])),
			}
	else:
		registered = {
			'DPS': (('registered', dps),),
			'Tanks': (('registered', tanks),),
			'Healers': (('registered', healers),)
			}
	return render_to_response('raid/view.djhtml',
							  {'raid': raid,
							   'registered': registered,
							   'registration_form': form,
							   'is_registered': raid.is_registered(request.user)
							   },
							  context_instance=RequestContext(request))

def create_user(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			User.objects.create_user(form.cleaned_data['username'], '', form.cleaned_data['password1'])
			return HttpResponseRedirect(reverse('home'))
		else:
			return render_to_response('home/signup.djhtml', {'form': form}) 
	else:
		return render_to_response('home/signup.djhtml', {'form': UserCreationForm()}, context_instance=RequestContext(request))

def logout_user(request):
	logout(request)
	return HttpResponseRedirect(reverse('home'))
