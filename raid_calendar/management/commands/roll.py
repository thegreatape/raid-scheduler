from django.core.management.base import BaseCommand
from raid_calendar.models import Raid
from raid_calendar import test
class Command(BaseCommand):
	def handle(self, *test_labels, **options):
		test.make_test_registrations()
		Raid.objects.all()[0].roll()
