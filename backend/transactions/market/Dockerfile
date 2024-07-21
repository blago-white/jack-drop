FROM python:3.11.3-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN adduser -D -u 1000 app --home /home/app/

WORKDIR /home/app/

COPY ../market /home/app/market/
COPY ../requirements.txt /home/app/requirements.txt
COPY ../.env /home/app/.env

RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

WORKDIR /home/app/market/

RUN chown -R app:app /home/app/market/

USER app

ENTRYPOINT ./start.sh
