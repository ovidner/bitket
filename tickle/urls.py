# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from tickle.views.products import PurchaseView, ShoppingCartView, ShoppingCartDeleteView, add_to_shopping_cart, \
    complete_purchase

urlpatterns = patterns(
    '',
    url(r'^purchase/$', PurchaseView.as_view(), name='purchase'),
    url(r'^purchase/complete/$', complete_purchase, name='complete_purchase'),
    url(r'^purchase/completed/$', TemplateView.as_view(template_name='tickle/purchase_completed.html'),
        name='purchase_completed_success'),

    url(r'^shoppingcart/add/(?P<pk>\d+)$', add_to_shopping_cart, name='shopping_cart_add'),
    url(r'^shoppingcart/remove/(?P<pk>\d+)$', ShoppingCartDeleteView.as_view(), name='shopping_cart_remove'),

)
