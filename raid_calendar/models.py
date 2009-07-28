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
		for registration in Registration.objects.filter(raid=self):
			# roll 1-100 for everyone signed up
			registration.number = random.randrange(100)
			# if player has culumlative weight, apply it 
			weight = registration.player.get_profile().weight
			registration.number += weight
			registration.applied_weight = weight
			registration.save()
		
		for role,spots in (("tank", self.tank_spots), ("healer", self.healer_spots), ("dps", self.dps_spots)):
			registered = Registration.objects.filter(raid=self,role=role,standby=False).order_by('-number')
			num_won = 0
			for registration in registered:
				player = registration.player
				profile = player.get_profile()
				if num_won < spots:
					registration.won = True
					profile.weight = 0
					num_won += 1
					print "%s won for %s, setting weight to 0" % (player, role)
				else:
					registration.won = False
					profile.weight += 20
					print "%s lost for %s, adding 20 to weight (now %i)" % (player, role, profile.weight)
				registration.save()
				player.save()
				profile.save()

			# couldn't fill in won spots with non-standbys, give spots to standbys
			standbys = Registration.objects.filter(raid=self,role=role,standby=True).order_by('-number')
			for standby in standbys:
				player = standby.player
				if num_won < spots:
					standby.won = True
					print "%s won for %s on standby (weight unchanged)" % (player, role)
					num_won += 1
				else:
					standby.won = False
					print "%s is chillin' on standby for %s" % (player, role)
				standby.save()
					
			while num_won < spots:
				num_won += 1

		self.has_rolled = True
		self.save()

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

	def raw_number(self):
		return self.number - self.applied_weight

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	weight = models.IntegerField(default=0)

	def total_registrations(self):
		return Registration.objects.filter(player=self.user).count()

	def total_won(self):
		return Registration.objects.filter(player=self.user,won=True).count()
