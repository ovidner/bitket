#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sof15.settings")
    os.environ.setdefault("DEBUG", "true")
    os.environ.setdefault("SECRET_KEY", "dev-unsafe")
    os.environ.setdefault("DATABASE_URL", "sqlite:///db.sqlite3")
    os.environ.setdefault('SENTRY_DSN', 'https://0df32cec564e4ba493eed0dd6c14f70f:041f90c127e849fcb42344bbb1565495@app.getsentry.com/36353')
    os.environ.setdefault('MANDRILL_API_KEY', 'EfHGUdoxJF878Ghwuf919A')  # This is just a test key, it won't actually send anything.

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
