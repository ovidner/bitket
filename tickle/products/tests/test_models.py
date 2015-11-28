from __future__ import absolute_import, unicode_literals

from django.test import TestCase

import stripe

class StripeMethodTests(TestCase):
    api_key='pk_test_crwDnA9V1JrrxQ8DB6H0JtFq'

    #Stripe tests
    def test_succesful_transaction_1(self):
        tok=stripe.Token.create(
            card={
                "number": '4242424242424242',
                "exp_month": 12,
                "exp_year": 2018,
                "cvc": '123'
            },
        )
        try:
            stripe.Charge.create(
                api_key=self.api_key,
                amount=10,
                currency='sek',
                source=tok
                #Test adding organizer here?
            )
        except stripe.error.CardError:
            self.fail("Charge failed")


    def test_card_declined(self):
        tok=stripe.Token.create(
            card={
                "number": '4000000000000002',
                "exp_month": 12,
                "exp_year": 2018,
                "cvc": '123'
            },
        )
        #Would like to check that the error code is card_declined.
        #Im not sure how that can be done.
        self.assertRaises(stripe.error.CardError, stripe.Charge.create,
                            api_key=self.api_key,
                            amount=10,
                            currency='sek',
                            source=tok
                            #Test adding organizer here?
                         )

        def test_incorrect_number(self):
            tok=stripe.Token.create(
                card={
                    "number": '4242424242424241',
                    "exp_month": 12,
                    "exp_year": 2018,
                    "cvc": '123'
                },
            )
            self.assertRaises(stripe.error.CardError, stripe.Charge.create,
                                api_key=self.api_key,
                                amount=10,
                                currency='sek',
                                source=tok
                                #Test adding organizer here?
                             )

        def test_exp_month_invalid(self):
            tok=stripe.Token.create(
                card={
                    "number": '4242424242424242',
                    "exp_month": 13,
                    "exp_year": 2018,
                    "cvc": '123'
                },
            )
            self.assertRaises(stripe.error.CardError, stripe.Charge.create,
                                api_key=self.api_key,
                                amount=10,
                                currency='sek',
                                source=tok
                                #Test adding organizer here?
                             )

        def test_exp_year_invalid(self):
            tok=stripe.Token.create(
                card={
                    "number": '4242424242424242',
                    "exp_month": 13,
                    "exp_year": 1930,
                    "cvc": '123'
                },
            )
            self.assertRaises(stripe.error.CardError, stripe.Charge.create,
                                api_key=self.api_key,
                                amount=10,
                                currency='sek',
                                source=tok
                                #Test adding organizer here?
                             )

        def test_exp_month_invalid(self):
            tok=stripe.Token.create(
                card={
                    "number": '4242424242424242',
                    "exp_month": 12,
                    "exp_year": 2018,
                    "cvc": '99'
                },
            )
            self.assertRaises(stripe.error.CardError, stripe.Charge.create,
                                api_key=self.api_key,
                                amount=10,
                                currency='sek',
                                source=tok
                                #Test adding organizer here?
                             )








