
from south.db import db
from django.db import models
from raid_scheduler.raid_calendar.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'UserProfile'
        db.create_table('raid_calendar_userprofile', (
            ('id', models.AutoField(primary_key=True)),
            ('user', models.ForeignKey(orm['auth.User'], unique=True)),
        ))
        db.send_create_signal('raid_calendar', ['UserProfile'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'UserProfile'
        db.delete_table('raid_calendar_userprofile')
        
    
    
    models = {
        'raid_calendar.registration': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'number': ('models.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'player': ('models.ForeignKey', ['User'], {}),
            'raid': ('models.ForeignKey', ['Raid'], {}),
            'role': ('models.CharField', [], {'max_length': '256'}),
            'standby': ('models.BooleanField', [], {'default': 'False'})
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
            'user': ('models.ForeignKey', ['User'], {'unique': 'True'})
        }
    }
    
    complete_apps = ['raid_calendar']
