FROM alpine:edge

RUN mkdir /app
WORKDIR /app

ENV DJANGO_SETTINGS_MODULE=tickle.settings.production \
    PYTHONPATH=/app/tickle:$PYTHONPATH \
    PYTHONUNBUFFERED=true

COPY ./requirements.alpine.txt /app/requirements.alpine.txt
RUN apk add --no-cache $(grep -vE "^\s*#" /app/requirements.alpine.txt | tr "\n" " ") && \
    ln -sf /usr/bin/python3 /usr/bin/python && \
    pip3 install --no-cache-dir -U pip setuptools wheel

COPY ./requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 80
CMD ["/app/run-django.sh"]
