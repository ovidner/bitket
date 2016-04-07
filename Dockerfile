FROM python:2.7
ENV DEBIAN_FRONTEND=noninteractive \
    DJANGO_SETTINGS_MODULE=config.settings.default \
    GUNICORN_PORT=8000 \
    PYTHONPATH=/app:$PYTHONPATH \
    PYTHONUNBUFFERED=true \
    PYTHONWARNINGS=ignore::DeprecationWarning

WORKDIR /app

ADD ./requirements.apt /app/requirements.apt

# See http://askubuntu.com/questions/252734/apt-get-mass-install-packages-from-a-file
RUN apt-get update && \
    apt-get install -y --no-install-recommends $(grep -vE "^\s*#" /app/requirements.apt  | tr "\n" " ") && \
    rm -rf /var/lib/apt/lists/*

# Requirements have to be pulled and installed here, otherwise caching won't work
ADD ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

#ADD ./package.json /app/package.json
#RUN

RUN groupadd -r django && useradd -r -g django django
ADD . /app
RUN chown -R django /app

RUN chmod +x /app/run/django /app/run/celery-beat /app/run/celery-worker /app/run/tests

RUN django-admin compilemessages

USER django
EXPOSE $GUNICORN_PORT

CMD ["/app/run/django"]
