from django.contrib.auth.models import User
from models import Raid, Registration
import random

def make_test_users():
	players = ['ncundeadmage',
			   'Airmid',
			   'Morgarn',
			   'Locrion',
			   'Drakkos',
			   'Vindo',
			   'Rhya',
			   'Vine',
			   'Ularen',
			   'Curwen',
			   'Vashron',
			   'peacelily',
			   'Ode',
			   'tormat',
			   'asphalt',
			   'Bifron',
			   'Bazra',
			   'EArcher',
			   'Kurogane',
			   'Zathe',
			   'Torkers',
			   'Latro']
	for player in players:
		user = User.objects.create_user(player,'', 'changeme')

def make_test_registrations():
	raid = Raid.objects.all()[0]
	raid.registered.clear()
	raid.has_rolled = False
	for player in User.objects.all():
		registration = Registration(player=player,
					    raid=raid,
					    standby=not random.randrange(10),
					    role=['dps', 'tank', 'healer'][random.randrange(3)])
		registration.save()
	raid.save()
