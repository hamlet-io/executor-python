FROM python:3.7-alpine AS base

COPY . /gen3-cli
WORKDIR /gen3-cli
RUN apk update && apk upgrade && apk add make && apk add bash

FROM base as dev

RUN pip install -r requirements/dev.txt -r requirements/prod.txt
CMD tail -f -s 60 /dev/null
