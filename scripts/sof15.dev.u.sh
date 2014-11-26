#!/bin/bash

sudo apt-get install -y python-dev python-pip libpq-dev libldap2-dev libsasl2-dev

# Has to be done manually to activate virtualenvwrapper etc.
source ~/.bash_profile

mkvirtualenv sof15
workon sof15

cd /vagrant/apps/sof15/
pip install -Ur requirements.txt

