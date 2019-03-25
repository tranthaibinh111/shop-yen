FROM python:3.7.2

ENV PYTHONUNBUFFERED 1

ADD ./requirements.txt /
RUN pip install -r requirements.txt

ADD ./compose/django/start.sh /
RUN sed -i 's/\r//' start.sh
RUN chmod +x start.sh

ADD . /app
RUN chmod +x app/manage.py
WORKDIR /app
