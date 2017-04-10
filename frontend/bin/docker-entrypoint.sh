#!/bin/sh
# Fail on non-zero exit status
set -e

# All environment variables are read at *build* time, which means we must build
# here and not during the Docker build phase.
yarn run build

exec "$@"
