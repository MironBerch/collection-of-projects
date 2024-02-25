FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app

WORKDIR /app

COPY requirements/requirements.txt requirements.txt
COPY ./requirements/requirements.lint.txt ./requirements.lint.txt

RUN pip install --upgrade pip-tools
RUN pip-sync requirements.txt requirements.*.txt

EXPOSE 8000

COPY . .
