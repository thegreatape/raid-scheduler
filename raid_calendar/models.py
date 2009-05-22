from django.contrib.auth.models import User
from django.db import models

class Raid(models.Model):
	title = models.CharField(max_length=256)
	date = models.DateTimeField('date/time of the raid')
	registered = models.ManyToManyField(User, related_name="registered_raiders")
	guaranteed_spots = models.ManyToManyField(User, related_name="guaranteed_spots")
	standby_spots = models.ManyToManyField(User, related_name="standby_spots")
	raid_leader = models.ForeignKey(User)
