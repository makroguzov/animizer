FROM python:3.10-slim

LABEL MAINTAINER="Valery Makroguzov valera.nedbai@gmail.com"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ARG PROJECT_DIR
ARG USER

ENV USER=$USER
ENV PROJECT_DIR=$PROJECT_DIR

COPY .  $PROJECT_DIR
WORKDIR $PROJECT_DIR

RUN echo Install dependencies using $(python -V) \
    # Установим зависимости
    && pip install --upgrade pip pipenv \
    && pipenv install --system --deploy \
    # Создадим нового пользователя
    && adduser \
          --no-create-home \
          --disabled-password  \
          --gecos "" $USER && chown -R $USER $PROJECT_DIR \
    # Дадим права на выполнение скрипта
    # Добавим ссылочку, что бы вызывать по красоте
    && echo -e '#!/bin/bash\npython -m src.main "$@"' > /usr/bin/playground \
    && chmod +x ./src/main.py \
    && chmod +x /usr/bin/playground

USER $USER
