FROM ubuntu:trusty
MAINTAINER Olle Vidner <olle.vidner@sof15.se>

ENV APP_NAME sof15
EXPOSE 8000

RUN apt-get update -y && apt-get install -y \
    python-dev \
    python-pip \
    libpq-dev \
    libldap2-dev \
    libsasl2-dev

RUN pip install virtualenv

RUN adduser --disabled-password $APP_NAME

USER $APP_NAME
ENV HOME /home/$APP_NAME

RUN virtualenv /home/$APP_NAME

# Copies only the requirements file first so that it can be cached by Docker
COPY ./requirements.txt /home/$APP_NAME/app/requirements.txt

WORKDIR /home/$APP_NAME/app
RUN /bin/bash -c '. /home/$APP_NAME/bin/activate && \
    pip install -r requirements.txt'

# Now copy the rest of the code
COPY . /home/$APP_NAME/app

# Running gunicorn also enters the virtualenv, so we don't have to do that explicitly
CMD ["/home/sof15/bin/gunicorn", "sof15.wsgi", "-c", "/home/sof15/app/conf/gunicorn.py"]
