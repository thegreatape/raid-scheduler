from django.test import TestCase
from raid_calendar.models import *

class RegistrationTest(TestCase):
    fixtures = ['registration_test.json']

    def testFixtures(self):
        self.assertEqual(UserProfile.objects.all().count(), 24)
