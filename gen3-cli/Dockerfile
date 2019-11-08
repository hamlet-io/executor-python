# BASE IMAGE
FROM python:3.7-alpine AS base

COPY . /gen3-cli
WORKDIR /gen3-cli
RUN apk update && apk upgrade && apk add make && apk add bash

# DEV ENV IMAGE
FROM base as dev

RUN pip install -r requirements/dev.txt -r requirements/prod.txt

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH "$PYTHONPATH:/gen3-cli"

CMD tail -f -s 60 /dev/null
