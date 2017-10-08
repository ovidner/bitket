FROM alpine:edge

RUN mkdir /app
WORKDIR /app

ENV DJANGO_SETTINGS_MODULE=bitket.settings.production \
    PYTHONPATH=/app/bitket:$PYTHONPATH \
    PYTHONUNBUFFERED=true

COPY ./requirements.alpine.txt /app/requirements.alpine.txt
RUN apk add --no-cache $(grep -vE "^\s*#" /app/requirements.alpine.txt | tr "\n" " ") && \
    ln -sf /usr/bin/python3 /usr/bin/python && \
    pip3 install --no-cache-dir -U pip setuptools wheel

COPY ./requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

COPY . /app

RUN DJANGO_SECRET_KEY=build DJANGO_DATABASE_URL=sqlite://// DJANGO_REDIS_URL=redis:// DJANGO_EMAIL_URL=consolemail:// django-admin collectstatic --no-input

EXPOSE 80
ENTRYPOINT ["/app/bin/docker-entrypoint"]
CMD ["/app/bin/run-django"]
