FROM python:3.10-slim

COPY . /animizer

ARG HOST
ARG PORT

ENV HOST=$HOST \
    PORT=$PORT

RUN pip install --upgrade pip pipenv
RUN pipenv install --system --deploy

CMD gunicorn src.main:get_application --bind $HOST:$PORT
