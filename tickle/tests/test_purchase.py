from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .. import factories, models


class PurchaseTests(APITestCase):
    purchase_url = reverse('purchase-list')

    def test_purchase_with_access_code(self):
        user = factories.UserFactory()
        event = factories.EventFactory()
        ticket_type_1 = factories.TicketTypeFactory(
            event=event,
            price=100,
            is_published=True,
            is_generally_available=True,
            total_limit=700)
        ticket_type_2 = factories.TicketTypeFactory(
            event=event,
            price=50,
            is_published=True,
            is_generally_available=True,
            total_limit=250)
