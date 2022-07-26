#!/bin/sh


#python manage.py migrate --run-syncdb
#python manage.py loaddata dbdump.json
#python manage.py collectstatic --no-input

gunicorn web.wsgi:application --bind 0.0.0.0:8000 --reload  -w 4
