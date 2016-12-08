from pprint import pprint
from threading import Thread
from copy import deepcopy
from time import time

from django.conf import settings
from django.db import connections
from django.test.utils import CaptureQueriesContext
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APITransactionTestCase, APIClient
import stripe

from .. import factories, models


class StressTests(APITransactionTestCase):
    def test_purchases(self):
        num_threads = 75
        num_per_thread = 10
        url = reverse('purchase-list')
        users = factories.UserFactory.create_batch(num_threads*num_per_thread)
        event = factories.EventFactory()
        ticket_type_1 = factories.TicketTypeFactory(
            event=event,
            price=100,
            is_published=True,
            is_generally_available=True,
            max_total_quantity=700)
        ticket_type_2 = factories.TicketTypeFactory(
            event=event,
            price=50,
            is_published=True,
            is_generally_available=True,
            max_total_quantity=250)

        def get_request_data():
            stripe_token = stripe.Token.create(card={
                "number": '4242424242424242',
                "exp_month": 12,
                "exp_year": 2018,
                "cvc": '123'
            })

            return {
                'access_codes': [],
                'tickets': [
                    {
                        'ticket_type': reverse('tickettype-detail',
                                               kwargs={'pk': ticket_type_1.pk}),
                        'variation_choices': []
                    },
                    {
                        'ticket_type': reverse('tickettype-detail',
                                               kwargs={'pk': ticket_type_2.pk}),
                        'variation_choices': []
                    }
                ],
                'payment': {
                    'type': 'stripe',
                    'payload': stripe_token.id,
                    'amount': '150.00'
                },
                'user': {
                    'nin': '9011290799'
                }
            }

        responses = []

        def worker(num):
            for _ in range(num):
                client = APIClient()
                user = users.pop()
                client.force_authenticate(user)

                with CaptureQueriesContext(connections['default']) as cqc_1:
                    with CaptureQueriesContext(connections['default_serializable']) as cqc_2:
                        start_time = time()
                        response = client.post(url, data=get_request_data(), format='json')
                        end_time = time()
                        queries = len(cqc_1.captured_queries) + len(cqc_2.captured_queries)
                pprint(response.data)
                responses.append((start_time, end_time-start_time, queries, len(response.data['tickets'])))

        threads = []
        for _ in range(num_threads):
            thread = Thread(target=worker, kwargs={'num': num_per_thread})
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        pprint(sorted(responses, key=lambda x: x[0]))
        self.assertEqual(models.Ticket.objects.pending().count(), 0)
        self.assertEqual(models.Ticket.objects.count(), 950)
        self.assertEqual(models.Transaction.objects.count(), 700)
