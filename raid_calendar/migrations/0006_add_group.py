from django.contrib.auth.models import User, Permission, Group
from south.db import db
from django.db import models
from raid_scheduler.raid_calendar.models import *

class Migration:
    
    def forwards(self, orm):
        raider_group = Group.objects.get(name='Raider')
        for user in User.objects.all():
            if not user.is_staff:
                user.groups.add(raider_group)
                user.is_staff = True
                user.save()
    
    
    def backwards(self, orm):
        "Write your backwards migration here"
    
    
    models = {
        'raid_calendar.registration': {
            'applied_weight': ('models.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'number': ('models.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'player': ('models.ForeignKey', ['User'], {}),
            'raid': ('models.ForeignKey', ['Raid'], {}),
            'role': ('models.CharField', [], {'max_length': '256'}),
            'standby': ('models.BooleanField', [], {'default': 'False'}),
            'won': ('models.BooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'raid_calendar.raid': {
            'date': ('models.DateTimeField', ["'date/time of the raid'"], {}),
            'description': ('models.TextField', [], {}),
            'dps_spots': ('models.IntegerField', [], {}),
            'has_rolled': ('models.BooleanField', [], {'default': 'False'}),
            'healer_spots': ('models.IntegerField', [], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'registered': ('models.ManyToManyField', ['User'], {'related_name': '"registered_raiders"', 'through': '"Registration"', 'blank': 'True'}),
            'roll_date': ('models.DateTimeField', ["'time when spots will be automatically rolled for'"], {}),
            'tank_spots': ('models.IntegerField', [], {}),
            'title': ('models.CharField', [], {'max_length': '256'})
        },
        'raid_calendar.userprofile': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'user': ('models.ForeignKey', ['User'], {'unique': 'True'}),
            'weight': ('models.IntegerField', [], {'default': '0'})
        }
    }
    
    complete_apps = ['raid_calendar']
