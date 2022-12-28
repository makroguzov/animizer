FROM python:3.10-slim

COPY  . /animizer
WORKDIR /animizer

ARG HOST
ARG PORT

ENV HOST=$HOST \
    PORT=$PORT

RUN pip install --upgrade pip pipenv
RUN pipenv install --system --deploy

CMD gunicorn src.main:app --bind $HOST:$PORT
