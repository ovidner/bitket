# -*- coding: utf-8 -*-

# From http://sentry.readthedocs.org/en/latest/faq/index.html#how-do-i

# Bootstrap the Sentry environment
from sentry.utils.runner import configure
configure()

# Do something crazy
from sentry.models import User

user = User()
user.username = 'admin'
user.email = 'it@sof15.se'
user.is_superuser = True
user.set_password('bajsmacka')
user.save()