from _pydecimal import Decimal
from datetime import date

import stripe
from django.conf import settings
from django.contrib.auth.hashers import is_password_usable, make_password

from django.core import signing
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from hamcrest import assert_that, calling, raises, not_, equal_to
from rest_framework.test import APITestCase

from ..db.fields import DescriptionField, MoneyField, NameField, \
    NullCharField, SlugField, PasswordField
from ..factories import ProductModifierFactory, HoldingModifierFactory, \
    ConditionFactory, StudentUnionMemberConditionFactory, UserFactory, \
    StudentUnionFactory, TicketTypeFactory, TicketFactory, CartFactory
from ..people.factories import StudentUnionFactory, PersonFactory

from ..models import User, Ticket
from ..products.factories import ProductFactory, HoldingFactory
from ..utils import sign_state, unsign_state


class ProductModifierMethodTests(TestCase):
    def test_save(self):
        modifier = ProductModifierFactory.build()

        modifier.delta_amount = None
        modifier.delta_factor = None
        assert_that(calling(modifier.save), raises(ValidationError))

        modifier.delta_amount = Decimal('-100.00')
        modifier.delta_factor = Decimal('-0.5')
        assert_that(calling(modifier.save), raises(ValidationError))

        modifier.delta_amount = Decimal('-100.00')
        modifier.delta_factor = None
        assert_that(calling(modifier.save), not_(raises(ValidationError)))

        modifier.delta_amount = None
        modifier.delta_factor = Decimal('-0.5')
        assert_that(calling(modifier.save), not_(raises(ValidationError)))

    def test_delta(self):
        modifier = ProductModifierFactory.build()

        modifier.delta_amount = None
        modifier.delta_factor = None
        assert_that(modifier.delta(), equal_to((None, None)))

        modifier.delta_amount = Decimal('-100.00')
        modifier.delta_factor = Decimal('-0.5')
        assert_that(modifier.delta(), equal_to((None, None)))

        modifier.delta_amount = Decimal('-100.00')
        modifier.delta_factor = None
        assert_that(modifier.delta(), equal_to((Decimal('-100.00'), False)))

        modifier.delta_amount = None
        modifier.delta_factor = Decimal('-0.5')
        assert_that(modifier.delta(), equal_to((Decimal('-0.5'), True)))

    def test_real_delta(self):
        modifier = ProductModifierFactory.build(
            product__base_price=Decimal('1000.00'))

        modifier.delta_amount = None
        modifier.delta_factor = None
        assert_that(modifier.real_delta(), equal_to(None))

        modifier.delta_amount = Decimal('-100.00')
        modifier.delta_factor = Decimal('-0.5')
        assert_that(modifier.real_delta(), equal_to(None))

        modifier.delta_amount = Decimal('-100.00')
        modifier.delta_factor = None
        assert_that(modifier.real_delta(), equal_to(Decimal('-100.00')))

        modifier.delta_amount = None
        modifier.delta_factor = Decimal('-0.5')
        assert_that(modifier.real_delta(), equal_to(Decimal('-500.00')))

        modifier.delta_amount = None
        modifier.delta_factor = None
        assert_that(modifier.real_delta(Decimal('200.00')), equal_to(None))

        modifier.delta_amount = Decimal('-100.00')
        modifier.delta_factor = Decimal('-0.5')
        assert_that(modifier.real_delta(Decimal('200.00')), equal_to(None))

        modifier.delta_amount = Decimal('-100.00')
        modifier.delta_factor = None
        assert_that(modifier.real_delta(Decimal('200.00')),
                    equal_to(Decimal('-100.00')))

        modifier.delta_amount = None
        modifier.delta_factor = Decimal('-0.5')
        assert_that(modifier.real_delta(Decimal('200.00')),
                    equal_to(Decimal('-100.00')))


class HoldingModifierMethodTests(TestCase):
    def test_save(self):
        product_1 = TicketTypeFactory()
        product_2 = TicketTypeFactory()

        product_modifier = ProductModifierFactory(product=product_1)
        holding = TicketFactory(product=product_1)
        holding_modifier = HoldingModifierFactory.build(
            product_modifier=product_modifier,
            holding=holding)


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


class ConditionMethodTests(TestCase):
    def test_is_met(self):
        condition = ConditionFactory()
        assert_that(calling(condition.is_met), raises(Exception))


class StudentUnionMemberConditionTests(TestCase):
    def test_is_met(self):
        student_union = StudentUnionFactory()
        condition = StudentUnionMemberConditionFactory(
            student_union=student_union)
        person = UserFactory(
            student_union=None)
        assert_that(condition.is_met(person), equal_to(False))

        other_student_union = StudentUnionFactory()
        person.student_union = other_student_union
        assert_that(condition.is_met(person), equal_to(False))

        person.student_union = student_union
        assert_that(condition.is_met(person), equal_to(True))


class PersonManagerTests(TestCase):
    def test_create_user(self):
        person = User.objects.create_user(
            first_name='First name',
            last_name='Last name',
            email='email@domain.com',
            password='Password')
        person = User.objects.get(pk=person.pk)
        assert_that(person.first_name, equal_to('First name'))
        assert_that(person.last_name, equal_to('Last name'))
        assert_that(person.email, equal_to('email@domain.com'))
        assert_that(person.has_usable_password())

    def test_create_superuser(self):
        person = User.objects.create_superuser(
            first_name='First name',
            last_name='Last name',
            email='email@domain.com',
            password='Password')
        person = User.objects.get(pk=person.pk)
        assert_that(person.first_name, equal_to('First name'))
        assert_that(person.last_name, equal_to('Last name'))
        assert_that(person.email, equal_to('email@domain.com'))
        assert_that(person.is_staff)
        assert_that(person.is_superuser)
        assert_that(person.has_usable_password())


class PersonMethodTests(TestCase):
    def test_get_pid(self):
        person = UserFactory.build()

        person.birth_date, person.pid_code, person.pid_coordination = (
            date(1950, 1, 15), '0001', False)
        assert_that(person.pid, equal_to('19500115-0001'))

        person.birth_date, person.pid_code, person.pid_coordination = (
            date(1950, 1, 15), '0008', True)
        assert_that(person.pid, equal_to('19500175-0008'))

        person.birth_date, person.pid_code, person.pid_coordination = (
            date(2001, 1, 15), '0001', False)
        assert_that(person.pid, equal_to('20010115-0001'))

        person.birth_date, person.pid_code, person.pid_coordination = (
            date(2001, 1, 15), '0008', True)
        assert_that(person.pid, equal_to('20010175-0008'))

        person.birth_date, person.pid_code, person.pid_coordination = (
            date(2001, 1, 15), None, False)
        assert_that(person.pid, equal_to('20010115-0000'))

    def test_set_pid(self):
        person = UserFactory.build()

        person.pid = '500115-0000'
        assert_that(
            (person.birth_date, person.pid_code, person.pid_coordination),
            equal_to((date(1950, 1, 15), None, False)))

        person.pid = '19500115-0000'
        assert_that(
            (person.birth_date, person.pid_code, person.pid_coordination),
            equal_to((date(1950, 1, 15), None, False)))

        person.pid = '500115+0001'
        assert_that(
            (person.birth_date, person.pid_code, person.pid_coordination),
            equal_to((date(1850, 1, 15), '0001', False)))

        person.pid = '500115-0001'
        assert_that(
            (person.birth_date, person.pid_code, person.pid_coordination),
            equal_to((date(1950, 1, 15), '0001', False)))

        person.pid = '500115-T009'
        assert_that(
            (person.birth_date, person.pid_code, person.pid_coordination),
            equal_to((date(1950, 1, 15), 'T009', False)))

        person.pid = '19500115-T009'
        assert_that(
            (person.birth_date, person.pid_code, person.pid_coordination),
            equal_to((date(1950, 1, 15), 'T009', False)))

        person.pid = '19500115-0001'
        assert_that(
            (person.birth_date, person.pid_code, person.pid_coordination),
            equal_to((date(1950, 1, 15), '0001', False)))

        person.pid = '19500175-0008'
        assert_that(
            (person.birth_date, person.pid_code, person.pid_coordination),
            equal_to((date(1950, 1, 15), '0008', True)))

        person.pid = '20010115-0001'
        assert_that(
            (person.birth_date, person.pid_code, person.pid_coordination),
            equal_to((date(2001, 1, 15), '0001', False)))

        person.pid = '20010175-0008'
        assert_that(
            (person.birth_date, person.pid_code, person.pid_coordination),
            equal_to((date(2001, 1, 15), '0008', True)))

    def test_get_full_name(self):
        person = UserFactory.build(
            first_name='First',
            last_name='Last')
        assert_that(person.get_full_name(), equal_to('First Last'))

    def test_get_short_name(self):
        person = UserFactory.build(
            first_name='First',
            last_name='Last')
        assert_that(person.get_short_name(), equal_to('First L.'))


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
        person= UserFactory()
        person.liu_student_union = StudentUnionFactory()
        return person

    def create_person_ordinary(self):
        return UserFactory()
        #Create person who is not a part of any student organization

    def create_cart_with_simple_product(self, person):
        cart = CartFactory()
        cart.person = person
        product = TicketTypeFactory()
        holding = Ticket(person = person, product = product, cart = cart)
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


STRIPE_TOKEN_OK = stripe.Token.create(card={
    'number': '4242424242424242',
    'exp_month': 12,
    'exp_year': 2016,
    'cvc': '123'
})


class PurchaseCartViewTests(APITestCase):
    def test_purchase_cart(self):
        cart = CartFactory()
        for i in range(0,1):
            TicketFactory(cart=cart)

        url = reverse('cart-purchase', kwargs={'pk': cart.pk})
        self.client.force_authenticate(user=cart.person)
        response = self.client.patch(url, {'stripe_token': STRIPE_TOKEN_OK.id})
        assert_that(response.status_code, equal_to(200))
        assert_that(response.data['purchased'], not_(equal_to(None)))


class DescriptionFieldTests(TestCase):
    def test_init(self):
        field = DescriptionField()
        assert_that(field.blank, equal_to(True))

        field = DescriptionField(blank=False)
        assert_that(field.blank, equal_to(False))


class MoneyFieldTests(TestCase):
    def test_init(self):
        field = MoneyField()
        assert_that(field.max_digits, equal_to(12))
        assert_that(field.decimal_places, equal_to(2))

        field = MoneyField(max_digits=9, decimal_places=3)
        assert_that(field.max_digits, equal_to(9))
        assert_that(field.decimal_places, equal_to(2))


class NameFieldTests(TestCase):
    def test_init(self):
        field = NameField()
        assert_that(field.max_length, equal_to(64))

        field = NameField(max_length=32)
        assert_that(field.max_length, equal_to(32))

    def test_clean(self):
        field = NameField()
        assert_that(
            calling(field.clean).with_args(value='', model_instance=None),
            raises(ValidationError))
        assert_that(
            calling(field.clean).with_args(value='   ', model_instance=None),
            raises(ValidationError))
        assert_that(field.clean(value='test', model_instance=None),
                    equal_to('test'))
        assert_that(field.clean(value=' test ', model_instance=None),
                    equal_to('test'))


class NullCharFieldTests(TestCase):
    def test_init(self):
        field = NullCharField()
        assert_that(field.null, equal_to(True))
        assert_that(field.blank, equal_to(True))
        assert_that(field.default, equal_to(None))

        field = NullCharField(null=False, blank=False, default='')
        assert_that(field.null, equal_to(True))
        assert_that(field.blank, equal_to(True))
        assert_that(field.default, equal_to(None))

    def test_clean(self):
        field = NullCharField(max_length=4)
        assert_that(field.clean(value='', model_instance=None),
                    equal_to(None))
        assert_that(field.clean(value=' ', model_instance=None),
                    equal_to(' '))
        assert_that(field.clean(value='test', model_instance=None),
                    equal_to('test'))


class SlugFieldTests(TestCase):
    def test_init(self):
        field = SlugField()
        assert_that(field.max_length, equal_to(64))

        field = SlugField(max_length=32)
        assert_that(field.max_length, equal_to(32))


class PasswordFieldTests(TestCase):
    def test_clean(self):
        field = PasswordField()

        value = None
        clean_value = field.clean(value=value, model_instance=None)
        assert_that(clean_value, not_(equal_to(None)))
        assert_that(clean_value, not_(equal_to('')))
        assert_that(not_(is_password_usable(clean_value)))

        value = ''
        clean_value = field.clean(value=value, model_instance=None)
        assert_that(clean_value, not_(equal_to(None)))
        assert_that(clean_value, not_(equal_to('')))
        assert_that(not_(is_password_usable(clean_value)))

        value = make_password('test')
        clean_value = field.clean(value=value, model_instance=None)
        assert_that(clean_value, equal_to(value))
        assert_that(is_password_usable(clean_value))
