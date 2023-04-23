FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /social_apps

WORKDIR /social_apps

COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy the project
COPY . .


