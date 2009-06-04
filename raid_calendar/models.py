from django.contrib.auth.models import User
from django.db import models
import random

class Registration(models.Model):
	player = models.ForeignKey(User)
	role = models.CharField(max_length=256)
	number = models.IntegerField(blank=True, null=True)

	def __unicode__(self):
		return self.player.username

class Raid(models.Model):
	title = models.CharField(max_length=256)
	date = models.DateTimeField('date/time of the raid')
	roll_date = models.DateTimeField('time when spots will be automatically rolled for')
	registered = models.ManyToManyField(Registration, related_name="registered_raiders", blank=True)
	raid_leader = models.ForeignKey(User)
	dps_spots = models.IntegerField()
	tank_spots = models.IntegerField()
	healer_spots = models.IntegerField()

	def __unicode__(self):
		return self.title

	def url(self):
		return self.id

	def is_registered(self, player):
		return len(self.registered.filter(player=player))

	def has_rolled(self):
		return

	def roll(self):
		for role in ("tank", "healer", "dps"):
			registered = self.registered.filter(role=role)
			spots = range(1, registered.count()+1)
			random.shuffle(spots)
			for registration in zip(registered, spots):
				registration[0].number = registration[1]
				registration[0].save()
