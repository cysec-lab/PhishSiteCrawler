FROM python:3.12-alpine

ENV PYTHONIOENCODING utf-8
ENV TZ="Asia/Tokyo"
ENV LANG=C.UTF-8
ENV LANGUAGE=en_US:en_US

WORKDIR /app

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt