#!/bin/bash

sudo -u postgres psql -c "CREATE ROLE sentry PASSWORD 'md596b367271e02d52160365b9ca6d89c13' NOSUPERUSER NOCREATEDB NOCREATEROLE INHERIT LOGIN;"
sudo -u postgres createdb -E utf-8 sentry
sudo -u postgres psql -c "GRANT ALL ON DATABASE sentry TO sentry;"