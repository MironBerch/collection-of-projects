# Instagram Clone [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

## Technology stack:
HTML, CSS, Python 3, Django Framework 4.0, Celery
## Steps to be followed for first time use
- Run this command - it  download dependencies
```
pip install -r requirements.txt
```
- Run these commands - they create database
```
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
```
- Run this command - to create superuser
```
python manage.py createsuperuser
```
- Everything is done - now you can start the server
```
python manage.py runserver
```