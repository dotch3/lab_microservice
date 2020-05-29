FROM python:3.6-alpine
LABEL MAINTAINER="Jorge M <jorge.mercado1405@gmail.com>"

ADD . /code
WORKDIR /code


RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 5000
EXPOSE 27017
CMD ["python", "app.py","--bind", "0.0.0.0:5000"]
