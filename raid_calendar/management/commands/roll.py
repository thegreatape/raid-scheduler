from django.core.management.base import BaseCommand
from raid_calendar.models import Raid
from raid_calendar import test
from datetime import datetime 

class Command(BaseCommand):
	def handle(self, *test_labels, **options):
		for raid in Raid.objects.filter(has_rolled=False, roll_date__lt=datetime.now()):
			raid.roll()
