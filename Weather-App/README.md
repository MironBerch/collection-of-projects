# Weather-App [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
create at 21.04.22
## Technology stack:
HTML, CSS, Bootstrap, Python 3, requests, Django 4
## Screenshot:
![Weather-App](https://user-images.githubusercontent.com/106734953/188310967-4234ed56-a145-4f7c-8abc-aade383d1e39.png)
## Steps to be followed for first time use
- Run this command - it download requirements
```
pip install -r requirements.txt
```
- Run these commands - they create database
```
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
```
- Everything is done - now you can start the server
```
python manage.py runserver
```