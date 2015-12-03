from __future__ import absolute_import, unicode_literals


CART = {
    'person_pk': 'person__pk'
}

HOLDING = {
    'person_pk': 'person__pk',
    'cart_pk': 'cart__pk'
}

MAIN_EVENT = {
    'organizer_slug': 'organizer__slug'
}

PRODUCT = {
    'main_event_slug': 'main_event__slug',
    'organizer_slug': 'main_event__organizer__slug'
}

PRODUCT_VARIATION = {
    'product_slug': 'product__slug',
    'main_event_slug': 'product__main_event__slug',
    'organizer_slug': 'product__main_event__organizer__slug'
}

PRODUCT_VARIATION_CHOICE = {
    'variation_pk': 'variation__pk',
    'product_slug': 'variation__product__slug',
    'main_event_slug': 'variation__product__main_event__slug',
    'organizer_slug': 'variation__product__main_event__organizer__slug'
}
