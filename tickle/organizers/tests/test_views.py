from __future__ import absolute_import, unicode_literals

from django.core import signing
from django.test import TestCase
from django.test.client import RequestFactory

from hamcrest import *

from tickle.people.factories import PersonFactory
from ..views import StripeConnectCallbackView, sign_state, unsign_state


class UtilFunctionTests(TestCase):
    def test_sign_state(self):
        organizer_pk = 1
        session_key = 'session-key'
        state = [organizer_pk, session_key]

        signed_state = sign_state(organizer_pk=organizer_pk,
                                  session_key=session_key)
        unsigned_state = signing.loads(signed_state)

        assert_that(unsigned_state, equal_to(state))

    def test_unsign_state(self):
        organizer_pk = 1
        session_key = 'sessionkey'
        state = [organizer_pk, session_key]

        signed_state = signing.dumps(state)
        unsigned_state = unsign_state(signed_state)

        assert_that(unsigned_state, equal_to(state))
        assert_that(calling(unsign_state).with_args(signed_state, max_age=0),
                    raises(signing.SignatureExpired))
