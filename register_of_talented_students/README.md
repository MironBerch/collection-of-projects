# Register of talented students [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

## Technologies:
- python 3.10
- Django 4
- SQLite
- Bootstrap 5
- Nginx
- Docker 20.10
- docker-compose 1.20

## Start project:

To run docker containers you have to create `.env` file in the code directory.

### Example of `.env` file:

```dotenv
SECRET_KEY='django-insecure-8fajd3)on9ecoq&&8__eryh-d5sz@6!8ky3+y0u5k6gw8!q$^t'
DEBUG=1
```

### by using docker on local server
- Run this command - it redirects to the code directory
```
cd register_of_talented_students
```
- Run this command - it start docker compose
```
docker-compose up --build
```

## Documentation

- [Project documentation](./docs/README.md)

## License

This project is licensed under the terms of the MIT license.