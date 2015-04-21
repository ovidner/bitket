# -*- coding: utf-8 -*-
from django import template

from decimal import Decimal

register = template.Library()


@register.inclusion_tag('tickle/elements/price_table.html')
def price_table(request, product):
    person = request.user.person

    discounts = []
    price = product.price

    eligible_product_discounts = product.product_discounts.eligible(person).select_related('discount')

    for product_discount in eligible_product_discounts:
        discount = product_discount.discount
        delta = discount.delta(price)
        price -= delta
        discounts.append({'description': discount.description(),
                          'percent': discount.readable_discount_percent(),
                          'delta': delta})

    teasers = (
        {'description': 'Bli funkis! 1 pass: 25 % rabatt, 2 pass: 60 % rabatt', 'price': ''},
        {'description': 'Bli funkis, jobba två pass, få 60 % rabatt!', 'price': ''},
    )

    return {'product': product,
            'discounts': discounts,
            'price': price,
            'teasers': teasers,
            'person': person}
