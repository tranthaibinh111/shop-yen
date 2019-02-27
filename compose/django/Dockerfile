FROM python:3.5.2

ENV PYTHONUNBUFFERED 1

ADD ./requirements.txt /
RUN pip install -r requirements.txt

ADD ./compose/django/start.sh /
RUN chmod +x start.sh

ADD ./shop-yen-server /app
WORKDIR /app