from __future__ import absolute_import, unicode_literals

from django.test import TestCase
from django.conf import settings

from tickle import people

from tickle.products.factories import CartFactory, ProductFactory
from tickle.products.models import Holding

from tickle.people.factories import PersonFactory, StudentUnionFactory



import stripe

class StripeMethodTests(TestCase):

    def setUp(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def good_token(self):
        return stripe.Token.create(
            card={
                "number": '4242424242424242',
                "exp_month": 12,
                "exp_year": 2018,
                "cvc": '123'
            },
        )

    def declined_token(self):
        return stripe.Token.create(
            card={
                "number": '4000000000000002',
                "exp_month": 12,
                "exp_year": 2018,
                "cvc": '123'
            },
        )

    def incorrect_number_token(self):
        return stripe.Token.create(
                card={
                    "number": '4242424242424241',
                    "exp_month": 12,
                    "exp_year": 2018,
                    "cvc": '123'
                },
            )

    def invalid_exp_month_token(self):
        stripe.Token.create(
                card={
                    "number": '4242424242424242',
                    "exp_month": 13,
                    "exp_year": 2018,
                    "cvc": '123'
                },
            )

    def invalid_exp_year_token(self):
        return stripe.Token.create(
                card={
                    "number": '4242424242424242',
                    "exp_month": 12,
                    "exp_year": 1930,
                    "cvc": '123'
                },
            )

    def invalid_cvc_token(self):
        return stripe.Token.create(
                card={
                    "number": '4242424242424242',
                    "exp_month": 12,
                    "exp_year": 2018,
                    "cvc": '99'
                },
            )

    def create_person_student_union(self):
        person= PersonFactory()
        person.liu_student_union = StudentUnionFactory()
        return person

    def create_person_ordinary(self):
        return PersonFactory()
        #Create person who is not a part of any student organization

    def create_cart_with_simple_product(self, person):
        cart = CartFactory()
        cart.person = person
        product = ProductFactory()
        holding = Holding(person = person, product = product, cart = cart)
        holding.save()
        return cart

        #Create a cart for person with a simple product


    def test_simple_product_succes(self):
        person = self.create_person_ordinary()
        cart = self.create_cart_with_simple_product(person)
        stripe_tok = self.good_token()
        cart.purchase(stripe_tok)
        assert(cart.purchased)

    def test_simple_product_fail(self):
        person = self.create_person_ordinary()
        cart = self.create_cart_with_simple_product(person)
        stripe_tok=self.declined_token()
        cart.purchase(stripe_tok)
        assert(cart.purchased == None)


    #Stripe tests
    def test_succesful_transaction_1(self):
        tok=self.good_token()
        try:
            stripe.Charge.create(
                amount=300,
                currency='sek',
                source=tok
                #Test adding organizer here?
            )
        except stripe.error.CardError:
            self.fail("Charge failed")


        def test_card_declined(self):
            tok=self.declined_token()
            #Would like to check that the error code is card_declined.
            #Im not sure how that can be done.
            self.assertRaises(stripe.error.CardError, stripe.Charge.create,
                                amount=300,
                                currency='sek',
                                source=tok
                                #Test adding organizer here?
                             )

        def test_incorrect_number(self):
            tok=self.incorrect_number_token()
            self.assertRaises(stripe.error.CardError, stripe.Charge.create,
                                amount=300,
                                currency='sek',
                                source=tok
                                #Test adding organizer here?
                             )

        def test_exp_month_invalid(self):
            tok=self.invalid_exp_month_token()
            self.assertRaises(stripe.error.CardError, stripe.Charge.create,
                                amount=300,
                                currency='sek',
                                source=tok
                                #Test adding organizer here?
                             )

        def test_exp_year_invalid(self):
            tok=self.invalid_exp_year_token()
            self.assertRaises(stripe.error.CardError, stripe.Charge.create,
                                amount=300,
                                currency='sek',
                                source=tok
                                #Test adding organizer here?
                             )

        def test_cvc_invalid(self):
            tok=self.invalid_cvc_token()
            self.assertRaises(stripe.error.CardError, stripe.Charge.create,
                                amount=300,
                                currency='sek',
                                source=tok
                                #Test adding organizer here?
                             )








