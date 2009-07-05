from django.contrib.auth.models import User
from django.db import models
import random

class Raid(models.Model):
	title = models.CharField(max_length=256)
	description = models.TextField()
	date = models.DateTimeField('date/time of the raid')
	roll_date = models.DateTimeField('time when spots will be automatically rolled for')
	registered = models.ManyToManyField(User, related_name="registered_raiders", blank=True, through="Registration")
	dps_spots = models.IntegerField()
	tank_spots = models.IntegerField()
	healer_spots = models.IntegerField()
	has_rolled = models.BooleanField(default=False)

	def __unicode__(self):
		return self.title

	def url(self):
		return self.id

	def is_registered(self, player):
		return len(self.registered.filter(username=player.username))

	def roll(self):
		for role,spots in (("tank", self.tank_spots), ("healer", self.healer_spots), ("dps", self.dps_spots)):
			# determine guaranteed spots -> those not on standby will be first
			registered = Registration.objects.filter(raid=self,role=role).order_by('standby')
			self._assign(registered, 1, spots+1)

			# shuffle in standbys with those who didn't get guaranteed spots
			standbys = Registration.objects.filter(raid=self,role=role,number=None)
			self._assign(standbys, spots+1, spots+standbys.count()+1)
		self.has_rolled = True
		self.save()
			
	def _assign(self, registered, start, end):
		if registered.count():
			spots = range(start, end)
			random.shuffle(spots)
			for registration in zip(registered, spots):
				registration[0].number = registration[1]
				registration[0].save()


class Registration(models.Model):
	raid = models.ForeignKey(Raid)
	player = models.ForeignKey(User)
	role = models.CharField(max_length=256)
	number = models.IntegerField(blank=True, null=True)
	applied_weight = models.IntegerField(blank=True, null=True)
	standby = models.BooleanField(default=False)
	won = models.BooleanField(blank=True, null=True)

	def __unicode__(self):
		return self.player.username

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	weight = models.IntegerField(default=0)

	def total_registrations(self):
		return Registration.objects.filter(player=self.user).count()
