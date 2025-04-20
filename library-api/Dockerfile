FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install poetry==1.8.4

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-root --no-interaction --no-ansi -vvv

COPY . .
