#!/bin/bash

ln -sf /vagrant/apps/sof15/sof15/conf/supervisor.conf /etc/supervisor/conf.d/sof15.dev.conf

service supervisor restart