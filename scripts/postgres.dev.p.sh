#!/bin/bash

echo "listen_addresses = '*'" >> /etc/postgresql/9.3/main/postgresql.conf
echo "host all all 0.0.0.0/0 md5"  >> /etc/postgresql/9.3/main/pg_hba.conf
service postgresql restart