from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

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
		print request.POST
		if form.is_valid():
			registration = Registration(player=request.user,
										role=form.cleaned_data['role'])
			registration.save()
			raid.registered.add(registration)
			raid.save()
	else:
		form = RegistrationForm()
	return render_to_response('raid/view.djhtml',
							  {'raid': raid,
							   'registered': raid.registered.all().order_by("role", "number"),
							   'registration_form': form,
							   'is_registered': raid.is_registered(request.user)},
							  context_instance=RequestContext(request))


def create_user(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			User.objects.create_user(form.cleaned_data['username'], '', form.cleaned_data['password1'])
			return HttpResponseRedirect('/')
		else:
			return render_to_response('home/signup.djhtml', {'form': form}) 
	else:
		return render_to_response('home/signup.djhtml', {'form': UserCreationForm()}, context_instance=RequestContext(request))

def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/')
