# syntax=docker/dockerfile:1
FROM ubuntu:22.04
COPY . /app

RUN apt update \
    && apt -y install slapd ldap-utils

CMD python /app/app.py