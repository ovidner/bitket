from uuid import UUID

from django.conf import settings
from django.core import signing
from six import text_type


def sign_state(organizer_pk, session_key):
    # Casts the UUID object to str
    if isinstance(organizer_pk, UUID):
        organizer_pk = text_type(organizer_pk)

    return signing.dumps([organizer_pk, session_key])


def unsign_state(state, max_age=None):
    if max_age is None:
        max_age = settings.STRIPE_OAUTH_SIGN_MAX_AGE

    return signing.loads(state, max_age=max_age)
