FROM python:3.12.2-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN adduser -D -u 1000 app --home /home/chat/

WORKDIR /home/chat/

COPY . .

RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

WORKDIR /home/chat/chat/

RUN chown -R app:app /home/chat/chat/
RUN chmod -R 744 /home/chat/chat/static/

RUN chmod 744 /home/chat/chat/debug.log
RUN chmod 744 /home/chat/chat/start.sh

USER app

ENTRYPOINT ./start.sh
