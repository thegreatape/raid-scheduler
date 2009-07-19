#!/bin/bash
python manage.py syncdb
python manage.py migrate raid_calendar 0001 --fake
python manage.py migrate raid_calendar
