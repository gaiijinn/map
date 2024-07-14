FROM python:3.9-alpine3.16

RUN apk add postgresql-client build-base postgresql-dev

COPY requirements.txt /temp/requirements.txt
COPY map_project /service

WORKDIR /service
EXPOSE 8000

RUN pip install --upgrade pip && \
    pip install -r /temp/requirements.txt

RUN adduser --disabled-password service-user

USER service-user
