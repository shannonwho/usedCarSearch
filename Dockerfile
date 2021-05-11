FROM ubuntu:18.04 as base

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev git

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 5000
CMD gunicorn --workers 4 --threads 2 -b 0.0.0.0:5000 'app:app'

FROM locustio/locust AS test

WORKDIR /test
COPY . /test

RUN pip3 install -r locust/requirements.txt 

ADD . /test/