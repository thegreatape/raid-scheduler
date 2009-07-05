import datetime
from south.db import db
from django.db import models
from raid_scheduler.raid_calendar.models import *

class Migration:

    def forwards(self, orm):
        for raid in orm.Raid.objects.all().order_by('date'):
            for registration in orm.Registration.objects.filter(raid=raid):
                profile = orm.UserProfile.objects.get(user=registration.player)
                if registration.role == 'dps' and registration.number > raid.dps_spots:
                    registration.won = False
                    if not registration.standby:
                        profile.weight += 20
                elif registration.role == 'tank' and registration.number > raid.tank_spots:
                    registration.won = False
                    if not registration.standby:
                        profile.weight += 20
                elif registration.role == 'healer' and registration.number > raid.healer_spots:
                    registration.won = False
                    if not registration.standby:
                        profile.weight += 20
                else:
                    registration.won = True
                    profile.weight = 0
                registration.save()
                profile.save()
    
    def backwards(self, orm):
        for registration in orm.Registration.objects.all():
            registration.won = None
            registration.save()
        for profile in orm.UserProfile.objects.all():
            profile.weight = 0
            profile.save()
    
    models = {
        'auth.message': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'message': ('models.TextField', ["_('message')"], {}),
            'user': ('models.ForeignKey', ['User'], {})
        },
        'auth.user': {
            'date_joined': ('models.DateTimeField', ["_('date joined')"], {'default': 'datetime.datetime.now'}),
            'email': ('models.EmailField', ["_('e-mail address')"], {'blank': 'True'}),
            'first_name': ('models.CharField', ["_('first name')"], {'max_length': '30', 'blank': 'True'}),
            'groups': ('models.ManyToManyField', ['Group'], {'verbose_name': "_('groups')", 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('models.BooleanField', ["_('active')"], {'default': 'True'}),
            'is_staff': ('models.BooleanField', ["_('staff status')"], {'default': 'False'}),
            'is_superuser': ('models.BooleanField', ["_('superuser status')"], {'default': 'False'}),
            'last_login': ('models.DateTimeField', ["_('last login')"], {'default': 'datetime.datetime.now'}),
            'last_name': ('models.CharField', ["_('last name')"], {'max_length': '30', 'blank': 'True'}),
            'password': ('models.CharField', ["_('password')"], {'max_length': '128'}),
            'user_permissions': ('models.ManyToManyField', ['Permission'], {'verbose_name': "_('user permissions')", 'blank': 'True'}),
            'username': ('models.CharField', ["_('username')"], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label','codename')", 'unique_together': "(('content_type','codename'),)"},
            'codename': ('models.CharField', ["_('codename')"], {'max_length': '100'}),
            'content_type': ('models.ForeignKey', ['ContentType'], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', ["_('name')"], {'max_length': '50'})
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
        },
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
        'auth.group': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', ["_('name')"], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('models.ManyToManyField', ['Permission'], {'verbose_name': "_('permissions')", 'blank': 'True'})
        }
    }
    
    complete_apps = ['raid_calendar', 'auth']
