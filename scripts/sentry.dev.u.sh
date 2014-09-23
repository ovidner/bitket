#!/bin/bash

sudo apt-get install -y python-dev python-pip libpq-dev libxslt1-dev libxml2-dev

# Has to be done manually to activate virtualenvwrapper etc.
source ~/.bash_profile

mkvirtualenv sentry
workon sentry

cd /vagrant/sentry/
pip install -Ur requirements.txt

export SENTRY_CONF=/vagrant/sentry/sentry.conf.py

sentry upgrade
python setup_dev.py
sentry repair --owner=admin

sudo ln -f -s /vagrant/sentry/supervisor.conf /etc/supervisor/conf.d/sentry.conf

sudo supervisorctl reload