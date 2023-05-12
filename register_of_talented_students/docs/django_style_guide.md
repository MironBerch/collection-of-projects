# Django guides


## Project structure

Example for project:
```
register_of_talented_students
|
└───config
|   |   __init__.py
|   |   settings.py
|   |   urls.py
|   |   wsgi.py
|
└───app
|   |   __init__.py
|   |   apps.py
|   |   views.py
│
└───templates
│   │   base.html
│   └───app
│       │   list.html
|       │   detail.html
|
└───.env.dev
|
└───docker-compose.yml
|
└───Dockerfile
|
└───manage.py
|
└───requirements.txt
```

## App structure

Example for app:
```
app
|───__init__.py
|───admin.py
|───apps.py
|───forms.py
|───models.py
|───services.py
|───urls.py
|───views.py
│
└───tests
│   │   test_services.py
│   │   test_views.py
│
└───migrations
│   │   __init__.py
│   │   0001_initial.py
```

## Models

Models should take care of the data model and not much else.

Do not put any business logic in model methods (there are only a few exceptions).

## Business logic

- Store business logic in `services.py` file or in a `service/` package.
- A service can be:
  - A simple function
  - A class
  - An entire module
- Methods and functions from `services.py` files are called only with positional arguments.
- Service functions take keyword-only arguments
- Services are type-annotated
- A service does business logic - from simple model creation to complex cross-cutting concerns, to calling external services & tasks