from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.urlresolvers import reverse

import calendar
from calendar import Calendar
from forms import RegistrationForm
from datetime import date, datetime, timedelta
from raid_calendar.models import Raid, Registration, UserProfile

def home(request):
	today = date.today()
	if request.method == 'GET' and 'year' in request.GET or 'month' in request.GET:
		today = date(year=int(request.GET.get('year', today.year)), month=int(request.GET.get('month', today.month)), day=today.day)

	days_in_month = calendar.mdays[today.month]
	raids = Raid.objects.filter(date__gte=datetime(today.year, today.month, 1)).exclude(date__gte=datetime(today.year, today.month, days_in_month))
	days = [{'day': x} for x in sum(Calendar().monthdayscalendar(today.year, today.month), [])]

	for raid in raids:
		event = days[days.index({'day': raid.date.day})]
		if "raids" in event:
			event["raids"].append(raid)
		else:
			event["raids"] = [raid]
	one_month = timedelta(days=days_in_month)
	forward = today + one_month
	back = today - one_month
	qstring = lambda d: 'month=%i&year=%i' % (d.month, d.year)
	
	context = {'date': today.strftime('%B %Y'),
		   'days' : days,
		   'nav' : {'forward': {'title': 'July 2009', 'qstring': qstring(forward), 'label': forward.strftime('%B %Y')},
			    'back'  : {'title': 'May 2009', 'qstring': qstring(back), 'label': back.strftime('%B %Y')}
			    }
		   }
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
			if 'standby' in form.cleaned_data:
				registration.standby = form.cleaned_data['standby'] 
			registration.save()
	else:
		form = RegistrationForm()

	dps = Registration.objects.filter(raid=raid,role="dps").order_by("-won", "-number")
	tanks = Registration.objects.filter(raid=raid,role="tank").order_by("-won", "-number")
	healers = Registration.objects.filter(raid=raid,role="healer").order_by("-won", "-number")

	registered = { 'DPS': dps,
		       'Tanks': tanks,
		       'Healers': healers
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
			user = User.objects.create_user(form.cleaned_data['username'], '', form.cleaned_data['password1'])
			profile = UserProfile(user=user)
			profile.save()
			raider_group = Group.objects.get(name='Raider')
			user.groups.add(raider_group)
			user.is_staff = True
			user.save()
			return HttpResponseRedirect(reverse('home'))
		else:
			return render_to_response('home/signup.djhtml', {'form': form}) 
	else:
		return render_to_response('home/signup.djhtml', {'form': UserCreationForm()}, context_instance=RequestContext(request))

def logout_user(request):
	logout(request)
	return HttpResponseRedirect(reverse('home'))

def users(request):
	return render_to_response('home/users.djhtml',
				  { 'users': User.objects.all().extra(select={'lower_username': 'lower(username)'}).order_by('lower_username')
				    },
				  context_instance=RequestContext(request))
