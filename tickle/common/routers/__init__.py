from __future__ import absolute_import, unicode_literals

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter as _DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from tickle.events.views import MainEventViewSet
from tickle.organizers.views import OrganizerViewSet
from tickle.people.views import PersonViewSet, StudentUnionViewSet
from tickle.products.views import (CartViewSet, HoldingViewSet, ProductViewSet,
                                   ProductVariationViewSet,
                                   ProductVariationChoiceViewSet)
from . import prefixes


class DefaultRouter(_DefaultRouter):
    include_format_suffixes = False


router = DefaultRouter()
router.register(prefixes.CART, CartViewSet)
router.register(prefixes.HOLDING, HoldingViewSet)
router.register(prefixes.ORGANIZER, OrganizerViewSet)
router.register(prefixes.PERSON, PersonViewSet)
router.register(prefixes.STUDENT_UNION, StudentUnionViewSet)

cart__router = NestedSimpleRouter(
    router, prefixes.CART, lookup='cart')
cart__router.register(prefixes.HOLDING, HoldingViewSet, base_name='cart-holding')

organizer__router = NestedSimpleRouter(
    router, prefixes.ORGANIZER, lookup='organizer')
organizer__router.register(prefixes.MAIN_EVENT, MainEventViewSet)

organizer__main_event__router = NestedSimpleRouter(
    organizer__router, prefixes.MAIN_EVENT, lookup='main_event')
organizer__main_event__router.register(prefixes.PRODUCT, ProductViewSet)

organizer__main_event__product__router = NestedSimpleRouter(
    organizer__main_event__router, prefixes.PRODUCT, lookup='product')
organizer__main_event__product__router.register(
    r'variations', ProductVariationViewSet)

organizer__main_event__product__variations__router = NestedSimpleRouter(
    organizer__main_event__product__router, r'variations', lookup='variation')
organizer__main_event__product__variations__router.register(
    r'choices', ProductVariationChoiceViewSet)

person__router = NestedSimpleRouter(router, prefixes.PERSON, lookup='person')
person__router.register(prefixes.CART, CartViewSet, base_name='person-cart')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(cart__router.urls)),
    url(r'^', include(organizer__router.urls)),
    url(r'^', include(organizer__main_event__router.urls)),
    url(r'^', include(organizer__main_event__product__router.urls)),
    url(r'^', include(organizer__main_event__product__variations__router.urls)),
    url(r'^', include(person__router.urls)),
]
