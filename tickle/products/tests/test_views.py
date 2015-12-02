from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse

from hamcrest import *
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
import stripe

from ..factories import CartFactory, HoldingFactory


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
            HoldingFactory(cart=cart)

        url = reverse('cart-purchase', kwargs={'pk': cart.pk})
        self.client.force_authenticate(user=cart.person)
        response = self.client.patch(url, {'stripe_token': STRIPE_TOKEN_OK.id})
        assert_that(response.status_code, equal_to(200))
        assert_that(response.data['purchased'], not_(equal_to(None)))

