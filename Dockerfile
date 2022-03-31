FROM python:3.9-alpine

COPY ./requirements.txt .

RUN pip install --upgrade pip

WORKDIR /usr/src/bic

RUN apk update \
    && apk add --update --no-cache --virtual build-deps gcc python3 musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk add --no-cache file-dev \
    && pip install filemagic \
    && apk add libc-dev linux-headers libffi-dev openssl-dev cargo \
#    && apk add libc-dev linux-headers libressl-dev  libffi-dev openssl-dev cargo \
    && apk add jpeg-dev zlib-dev libjpeg \
    && python3 -m pip install --upgrade cryptography \
    && pip install Pillow \
    && apk del build-deps

RUN pip install -r /requirements.txt

COPY ./ /usr/src/bic

COPY ./skote /


COPY ./entrypoint.sh /

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

EXPOSE 9193

ENTRYPOINT ["sh", "entrypoint.sh"]

