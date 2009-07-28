import random
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from raid_calendar.models import Raid, Registration
from raid_calendar import test
from datetime import datetime 

class Command(BaseCommand):
	def handle(self, *test_labels, **options):
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
            print "raid %s setup for testing" % raid
