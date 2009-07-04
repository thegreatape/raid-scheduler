
from south.db import db
from django.db import models
from raid_scheduler.raid_calendar.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Registration'
        db.create_table('raid_calendar_registration', (
            ('raid', models.ForeignKey(orm.Raid)),
            ('standby', models.BooleanField(default=False)),
            ('number', models.IntegerField(null=True, blank=True)),
            ('player', models.ForeignKey(orm['auth.User'])),
            ('role', models.CharField(max_length=256)),
            ('id', models.AutoField(primary_key=True)),
        ))
        db.send_create_signal('raid_calendar', ['Registration'])
        
        # Adding model 'Raid'
        db.create_table('raid_calendar_raid', (
            ('roll_date', models.DateTimeField('time when spots will be automatically rolled for')),
            ('dps_spots', models.IntegerField()),
            ('description', models.TextField()),
            ('title', models.CharField(max_length=256)),
            ('healer_spots', models.IntegerField()),
            ('has_rolled', models.BooleanField(default=False)),
            ('date', models.DateTimeField('date/time of the raid')),
            ('tank_spots', models.IntegerField()),
            ('id', models.AutoField(primary_key=True)),
        ))
        db.send_create_signal('raid_calendar', ['Raid'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Registration'
        db.delete_table('raid_calendar_registration')
        
        # Deleting model 'Raid'
        db.delete_table('raid_calendar_raid')
        
    
    
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
        }
    }
    
    complete_apps = ['raid_calendar']
