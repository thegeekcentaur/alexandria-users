FROM debian
LABEL maintainer="Guardians Of The Galaxy"
FROM python:3.9

# Change port per service
EXPOSE 9001

COPY ./app /app
WORKDIR /app/

COPY requirements.txt .
RUN pip3 install -Ir requirements.txt

COPY ./config/gunicorn_conf.py /gunicorn_conf.py
COPY ./start.sh /start.sh
RUN chmod +x /start.sh

ENV PYTHONPATH=/app

CMD ["/start.sh"]