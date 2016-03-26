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
    apt-get install -y $(grep -vE "^\s*#" /app/requirements.apt  | tr "\n" " ")

# Requirements have to be pulled and installed here, otherwise caching won't work
ADD ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

#ADD ./package.json /app/package.json
#RUN

RUN groupadd -r django && useradd -r -g django django
ADD . /app
RUN chown -R django /app

RUN chmod +x /app/docker/entrypoint.sh /app/docker/gunicorn.sh /app/docker/celery-beat.sh /app/docker/celery-worker.sh

RUN django-admin compilemessages

USER django
EXPOSE $GUNICORN_PORT

CMD ["/app/docker/gunicorn.sh"]
