FROM phusion/baseimage:0.9.15
MAINTAINER Olle Vidner <olle.vidner@sof15.se>

# Disable SSH
RUN rm -rf /etc/service/sshd /etc/my_init.d/00_regen_ssh_host_keys.sh

# Python, splitted out for caching
RUN apt-get update -y && apt-get install -y \
    python-dev \
    python-pip

# Other packages
RUN apt-get update -y && apt-get install -y \
    libpq-dev \
    libldap2-dev \
    libsasl2-dev \
    libncurses5-dev \
    git \
    gettext

RUN pip install virtualenv

# --gecos "" for non-interactive behavior
RUN adduser --disabled-password --gecos "" sof15

RUN virtualenv /home/sof15

# Copies only the requirements file first so that it can be cached by Docker
COPY ./requirements.txt /home/sof15/app/requirements.txt

RUN /home/sof15/bin/pip install -r /home/sof15/app/requirements.txt

# Now copy the rest of the code
COPY . /home/sof15/app

RUN mkdir -p /home/sof15/app/_build/static/

# Django will be sad if we don't set these envs during build.
ENV DEBUG true
ENV SECRET_KEY build
RUN /home/sof15/bin/python /home/sof15/app/manage.py collectstatic --noinput
RUN /home/sof15/bin/python /home/sof15/app/manage.py compilemessages
# "Unset" the SECRET_KEY, so we can't accidently start with an unsafe, default key
ENV SECRET_KEY ''
ENV DEBUG false

USER sof15
ENV HOME /home/sof15
WORKDIR /home/sof15/app

EXPOSE 8080

# Running gunicorn also enters the virtualenv, so we don't have to do that explicitly
CMD ["/home/sof15/bin/newrelic-admin", "run-program", "/home/sof15/bin/gunicorn", "sof15.wsgi", "-c", "/home/sof15/app/_conf/gunicorn.py"]
