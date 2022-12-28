FROM python:3.10-slim

COPY  . /animizer
WORKDIR /animizer

ARG HOST
ARG PORT

ENV HOST=$HOST \
    PORT=$PORT

RUN pip install --upgrade pip pipenv
RUN pipenv install --system --deploy
RUN python -m nltk.downloader stopwords

CMD gunicorn src.main:app \
        --workers 2 \
        --bind $HOST:$PORT \
        --worker-class uvicorn.workers.UvicornWorker

