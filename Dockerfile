FROM python:2.7
ENV DEBIAN_FRONTEND=noninteractive \
    DJANGO_SETTINGS_MODULE=config.settings.default \
    GUNICORN_PORT=8000 \
    PYTHONPATH=/app:$PYTHONPATH \
    PYTHONUNBUFFERED=true \
    PYTHONWARNINGS=ignore::DeprecationWarning

ADD ./requirements.apt /requirements.apt

# See http://askubuntu.com/questions/252734/apt-get-mass-install-packages-from-a-file
RUN apt-get update && \
    apt-get install -y $(grep -vE "^\s*#" /requirements.apt  | tr "\n" " ")

# Requirements have to be pulled and installed here, otherwise caching won't work
ADD ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN groupadd -r django && useradd -r -g django django
ADD . /app
RUN chown -R django /app

ADD ./docker/gunicorn.sh /gunicorn.sh
ADD ./docker/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh && chown django /entrypoint.sh
RUN chmod +x /gunicorn.sh && chown django /gunicorn.sh

WORKDIR /app
USER django
EXPOSE $GUNICORN_PORT
ENTRYPOINT ["/entrypoint.sh"]
CMD ["/gunicorn.sh"]
