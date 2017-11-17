import os

for (key, value) in dict(
    BITKET_EMAIL_URL='consolemail://',
    BITKET_SECRET_KEY='wowsuchsecret',
    BITKET_TEST_MODE='true',
).items():
    os.environ.setdefault(key, value)

from bitket.settings import *  # isort:skip
