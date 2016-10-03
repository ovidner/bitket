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
router.register(prefixes.MAIN_EVENT, MainEventViewSet)
router.register(prefixes.ORGANIZER, OrganizerViewSet)
router.register(prefixes.PERSON, PersonViewSet)
router.register(prefixes.PRODUCT, ProductViewSet)
router.register(prefixes.PRODUCT_VARIATION, ProductVariationViewSet)
router.register(prefixes.PRODUCT_VARIATION_CHOICE, ProductVariationChoiceViewSet)
router.register(prefixes.STUDENT_UNION, StudentUnionViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
