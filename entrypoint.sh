#!/bin/sh

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn --bind 0.0.0.0:9193 skote.wsgi:application
#uwsgi --socket :9194 --workers 4 --master --enable-threads --module skote.wsgi --static-map /static=/var/www/html/admin/assets/
