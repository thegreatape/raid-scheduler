
from south.db import db
from django.db import models
from raid_scheduler.raid_calendar.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Registration.won'
        db.add_column('raid_calendar_registration', 'won', models.BooleanField(null=True, blank=True))
        
        # Adding field 'Registration.applied_weight'
        db.add_column('raid_calendar_registration', 'applied_weight', models.IntegerField(null=True, blank=True))
        
        # Adding field 'UserProfile.weight'
        db.add_column('raid_calendar_userprofile', 'weight', models.IntegerField(default=0))
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Registration.won'
        db.delete_column('raid_calendar_registration', 'won')
        
        # Deleting field 'Registration.applied_weight'
        db.delete_column('raid_calendar_registration', 'applied_weight')
        
        # Deleting field 'UserProfile.weight'
        db.delete_column('raid_calendar_userprofile', 'weight')
        
    
    
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
