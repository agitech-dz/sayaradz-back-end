FROM python:3.7.2-alpine3.8

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 apk add jpeg-dev zlib-dev &&\
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps
CMD python manage.py runserver 0.0.0.0:$PORT
