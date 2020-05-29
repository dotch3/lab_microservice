FROM python:3.6-alpine
LABEL MAINTAINER="Jorge M <jorge.mercado1405@gmail.com>"

ADD . /code
WORKDIR /code

ENV MONGODB_DATABASE=admin
ENV MONGODB_USERNAME=root
ENV MONGODB_PASSWORD=boavizinhanca2020
ENV MONGODB_HOSTNAME=mongodb

# Database creds

ENV MONGO_INITDB_ROOT_USERNAME=root
ENV MONGO_INITDB_ROOT_PASSWORD=boavizinhanca2020
ENV MONGO_INITDB_DATABASE=admin
ENV MONGODB_DATA_DIR=/data/db
ENV MONDODB_LOG_DIR=/data/logs


RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 5000
EXPOSE 27017
CMD ["python", "app.py","--bind", "0.0.0.0:5000"]
