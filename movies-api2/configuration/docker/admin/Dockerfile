FROM python:3.12-alpine

WORKDIR /app

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements/requirements.admin.txt  /app/requirements.admin.txt
RUN pip install -r requirements.admin.txt

COPY . .

ENTRYPOINT ["/app/configuration/docker/admin/entrypoint.sh"]
