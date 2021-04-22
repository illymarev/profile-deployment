FROM python:3.9.4
MAINTAINER Illia Lymarev

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /DjangoProject
WORKDIR /DjangoProject
COPY ./DjangoProject /DjangoProject


