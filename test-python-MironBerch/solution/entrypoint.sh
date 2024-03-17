#!/bin/sh

python manage.py migrate users zero
python manage.py migrate api zero

python manage.py migrate
#python manage.py flush --no-input

python manage.py setup_countries

python manage.py runserver $SERVER_ADDRESS

exec "$@"