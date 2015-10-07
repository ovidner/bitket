# -*- coding: utf-8 -*-
from decimal import Decimal

from django.test import TestCase

from model_mommy import mommy
from hamcrest import *

from ..models import Invoice

class InvoiceQuerySetTests(TestCase):
    def test_annotate_total(self):
        invoice_1 = mommy.make('invar.Invoice')
        invoice_2 = mommy.make('invar.Invoice')
        invoice_3 = mommy.make('invar.Invoice')
        invoice_4 = mommy.make('invar.Invoice')
        invoice_5 = mommy.make('invar.Invoice')

        annotated_invoices = Invoice.objects.annotate_total()

        # Empty aggregates should be None, not 0
        assert_that(annotated_invoices.get(pk=invoice_1.pk).annotated_total,
                    equal_to(None))
        assert_that(annotated_invoices.get(pk=invoice_2.pk).annotated_total,
                    equal_to(None))
        assert_that(annotated_invoices.get(pk=invoice_3.pk).annotated_total,
                    equal_to(None))
        assert_that(annotated_invoices.get(pk=invoice_4.pk).annotated_total,
                    equal_to(None))
        assert_that(annotated_invoices.get(pk=invoice_5.pk).annotated_total,
                    equal_to(None))

        mommy.make(
            'invar.InvoiceRow',
            invoice=invoice_1,
            price=2,
            quantity=5,
            _quantity=19
        )
        mommy.make(
            'invar.InvoiceRow',
            invoice=invoice_1,
            price=7,
            quantity=3,
            _quantity=17
        )

        # Numbers with decimals
        # Not really primes, but primes divided by 100, so this should be pretty
        # safe too.
        mommy.make(
            'invar.InvoiceRow',
            invoice=invoice_2,
            price=Decimal('9824494.91'),
            quantity=3,
            _quantity=11
        )
        mommy.make(
            'invar.InvoiceRow',
            invoice=invoice_2,
            price=Decimal('9823777.03'),
            quantity=7,
            _quantity=521
        )

        # Pushing it
        mommy.make(
            'invar.InvoiceRow',
            invoice=invoice_3,
            price=1000037,
            quantity=1021127,
            _quantity=179
        )
        mommy.make(
            'invar.InvoiceRow',
            invoice=invoice_3,
            price=3207899,
            quantity=8313917,
            _quantity=269
        )
        mommy.make(
            'invar.InvoiceRow',
            invoice=invoice_3,
            price=9305057,
            quantity=9327887,
            _quantity=101
        )

        # Combining integers and decimals, positive and negative
        mommy.make(
            'invar.InvoiceRow',
            invoice=invoice_4,
            price=2837801,
            quantity=13,
            _quantity=2
        )
        mommy.make(
            'invar.InvoiceRow',
            invoice=invoice_4,
            price=-4989461,
            quantity=17,
            _quantity=5
        )
        mommy.make(
            'invar.InvoiceRow',
            invoice=invoice_4,
            price=Decimal('18304.19'),
            quantity=3,
            _quantity=641
        )
        mommy.make(
            'invar.InvoiceRow',
            invoice=invoice_4,
            price=Decimal('-17520.11'),
            quantity=7,
            _quantity=1151
        )

        # Free row
        mommy.make(
            'invar.InvoiceRow',
            invoice=invoice_5,
            price=0,
            quantity=1
        )

        annotated_invoices = Invoice.objects.annotate_total()

        assert_that(annotated_invoices.get(pk=invoice_1.pk).annotated_total,
                    equal_to(
                        (2 * 5 * 19) +
                        (7 * 3 * 17)
                        ))
        assert_that(annotated_invoices.get(pk=invoice_2.pk).annotated_total,
                    equal_to(
                        (Decimal('9824494.91') * 3 * 11) +
                        (Decimal('9823777.03') * 7 * 521)
                        ))
        assert_that(annotated_invoices.get(pk=invoice_3.pk).annotated_total,
                    equal_to(
                        (1000037 * 1021127 * 179) +
                        (3207899 * 8313917 * 269) +
                        (9305057 * 9327887 * 101)
                        ), 'Unexpected value. Please note: it seems like this '
                           'assertion normally fails with SQLite as backend.')
        assert_that(annotated_invoices.get(pk=invoice_4.pk).annotated_total,
                    equal_to(
                        (2837801 * 13 * 2) +
                        (-4989461 * 17 * 5) +
                        (Decimal('18304.19') * 3 * 641) +
                        (Decimal('-17520.11') * 7 * 1151)
                        ))
        assert_that(annotated_invoices.get(pk=invoice_5.pk).annotated_total,
                    equal_to(0))

    def test_annotate_payed(self):
        # This will also create Invoice objects
        handle_1 = mommy.make('invar.InvoiceHandle')
        handle_2 = mommy.make('invar.InvoiceHandle')

        annotated_invoices = Invoice.objects.annotate_payed()

        assert_that(
            annotated_invoices.get(pk=handle_1.invoice.pk).annotated_payed,
            equal_to(None))
        assert_that(
            annotated_invoices.get(pk=handle_2.invoice.pk).annotated_payed,
            equal_to(None))

        mommy.make(
            'invar.TransactionMatch',
            handle=handle_1,
            transaction=mommy.make(
                'invar.Transaction',
                amount=1500041
            )
        )
        mommy.make(
            'invar.TransactionMatch',
            handle=handle_1,
            transaction=mommy.make(
                'invar.Transaction',
                amount=1540787
            )
        )
        mommy.make(
            'invar.TransactionMatch',
            handle=handle_1,
            transaction=mommy.make(
                'invar.Transaction',
                amount=-7
            )
        )

        mommy.make(
            'invar.TransactionMatch',
            handle=handle_2,
            transaction=mommy.make(
                'invar.Transaction',
                amount=Decimal('9676306.81')
            )
        )
        mommy.make(
            'invar.TransactionMatch',
            handle=handle_2,
            transaction=mommy.make(
                'invar.Transaction',
                amount=Decimal('-6747.59')
            )
        )

        annotated_invoices = Invoice.objects.annotate_payed()

        assert_that(
            annotated_invoices.get(pk=handle_1.invoice.pk).annotated_payed,
            equal_to(
                1500041 + 1540787 - 7
            ))
        assert_that(
            annotated_invoices.get(pk=handle_2.invoice.pk).annotated_payed,
            equal_to(
                Decimal('9676306.81') - Decimal('6747.59')
            ))

    def test_payed(self):
        """
        Tests that:

        * Invoices with no rows and no payments are considered as payed
        * Invoices with totals over 0 and no payment are not considered as payed
        * Invoices with totals over 0 and with payments totalling to less than
        the invoice total are not considered as payed
        * Invoices with totals over 0 and with payments totalling to the invoice
        total are considered as payed
        * Invoices with totals over 0 and with payments totalling to more than
        the invoice total are not considered as payed
        """
        invoice_1 = mommy.make('invar.Invoice')
        invoice_2 = mommy.make('invar.Invoice')
        invoice_3 = mommy.make('invar.Invoice')

        handle_1 = mommy.make(
            'invar.InvoiceHandle',
            invoice=invoice_1
        )
        handle_2 = mommy.make(
            'invar.InvoiceHandle',
            invoice=invoice_2
        )
        handle_3 = mommy.make(
            'invar.InvoiceHandle',
            invoice=invoice_3
        )

        assert_that(
            Invoice.objects.payed(),
            contains_inanyorder(invoice_1, invoice_2, invoice_3))

        mommy.make(
            'invar.InvoiceRow',
            invoice=invoice_1,
            price=1000,
            quantity=1
        )
        mommy.make(
            'invar.InvoiceRow',
            invoice=invoice_2,
            price=1000,
            quantity=1
        )
        mommy.make(
            'invar.InvoiceRow',
            invoice=invoice_3,
            price=1000,
            quantity=1
        )

        assert_that(
            Invoice.objects.payed(),
            empty())

        mommy.make(
            'invar.TransactionMatch',
            handle=handle_1,
            transaction=mommy.make(
                'invar.Transaction',
                amount=900
            )
        )
        mommy.make(
            'invar.TransactionMatch',
            handle=handle_2,
            transaction=mommy.make(
                'invar.Transaction',
                amount=1000
            )
        )
        mommy.make(
            'invar.TransactionMatch',
            handle=handle_3,
            transaction=mommy.make(
                'invar.Transaction',
                amount=1100
            )
        )

        assert_that(
            Invoice.objects.payed(),
            only_contains(invoice_2))
