#!/bin/sh
python manage.py migrate
python manage.py search_index --rebuild -f
gunicorn 'back_end.wsgi' -b 0.0.0.0:80 --access-logfile - --log-level info
#python manage.py runserver 0.0.0.0:80
