FROM python:3.11-alpine

WORKDIR /app

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt  /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
