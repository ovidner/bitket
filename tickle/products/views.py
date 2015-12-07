from __future__ import absolute_import, unicode_literals

from rest_framework.generics import UpdateAPIView
from rest_framework.decorators import detail_route
from rest_framework.filters import DjangoFilterBackend
from rest_framework.response import Response

from tickle.common.routers import parent_lookups
from tickle.common.views import ModelViewSet
from .filters import (CartFilterBackend, HoldingFilterSet,
                      HoldingPermissionFilterBackend)
from .models import (Cart, Holding, Product, ProductVariation,
                     ProductVariationChoice)
from .serializers import (CartSerializer, CartPurchaseSerializer,
                          HoldingSerializer, ProductSerializer,
                          ProductVariationSerializer,
                          ProductVariationChoiceSerializer)


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    filter_backends = (CartFilterBackend,)
    parent_lookups = parent_lookups.CART

    def get_purchase_serializer(self, *args, **kwargs):
        serializer_class = CartPurchaseSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    @detail_route(['patch'])
    def purchase(self, request, pk=None):
        instance = self.get_object()
        purchase_serializer = self.get_purchase_serializer(instance, data=request.data, partial=True)
        purchase_serializer.is_valid(raise_exception=True)
        self.perform_update(purchase_serializer)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class HoldingViewSet(ModelViewSet):
    queryset = Holding.objects.all()
    serializer_class = HoldingSerializer
    filter_backends = (HoldingPermissionFilterBackend, DjangoFilterBackend)
    filter_class = HoldingFilterSet
    parent_lookups = parent_lookups.HOLDING

    @detail_route(['post', 'patch'])
    def utilize(self, request, pk=None):
        instance = self.get_object()
        instance.utilize()
        instance.save()
        return self.retrieve(request, pk=pk)

    @detail_route(['post', 'patch'])
    def unutilize(self, request, pk=None):
        instance = self.get_object()
        instance.unutilize()
        instance.save()
        return self.retrieve(request, pk=pk)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.published()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    parent_lookups = parent_lookups.PRODUCT


class ProductVariationViewSet(ModelViewSet):
    queryset = ProductVariation.objects.all()
    serializer_class = ProductVariationSerializer
    parent_lookups = parent_lookups.PRODUCT_VARIATION


class ProductVariationChoiceViewSet(ModelViewSet):
    queryset = ProductVariationChoice.objects.all()
    serializer_class = ProductVariationChoiceSerializer
    parent_lookups = parent_lookups.PRODUCT_VARIATION_CHOICE
