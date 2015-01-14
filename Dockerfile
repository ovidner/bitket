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
    git

RUN pip install virtualenv

# --gecos "" for non-interactive behavior
RUN adduser --disabled-password --gecos "" sof15

RUN virtualenv /home/sof15

# Copies only the requirements file first so that it can be cached by Docker
COPY ./requirements.txt /home/sof15/app/requirements.txt

WORKDIR /home/sof15/app
RUN /bin/bash -c '. /home/sof15/bin/activate && \
    pip install -r requirements.txt'

# Now copy the rest of the code
COPY . /home/sof15/app

RUN /home/sof15/bin/python /home/sof15/app/manage.py collectstatic --noinput

USER sof15
ENV HOME /home/sof15
EXPOSE 80

# Running gunicorn also enters the virtualenv, so we don't have to do that explicitly
CMD ["/home/sof15/bin/gunicorn", "sof15.wsgi", "-c", "/home/sof15/app/_conf/gunicorn.py"]
