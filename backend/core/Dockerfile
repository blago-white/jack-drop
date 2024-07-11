FROM python:3.11.3-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN adduser -D -u 1000 app --home /home/app/

WORKDIR /home/app/

COPY . .

RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

WORKDIR /home/app/core/

RUN chown -R app:app /home/app/core/
#RUN chmod -R 744 /home/app/core/debug.log

USER app

ENTRYPOINT ./start.sh
