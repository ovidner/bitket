from __future__ import absolute_import, unicode_literals
import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _

from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework import serializers
import stripe

from ..common import exceptions
from ..common.serializers import HyperlinkedModelSerializer
from ..modifiers.models import Modifier
from .models import Cart, Holding, Product, ProductVariation, ProductVariationChoice


class HoldingSerializer(HyperlinkedModelSerializer):
    price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    permissions = DRYPermissionsField(actions=['utilize', 'unutilize'])

    class Meta:
        model = Holding
        fields = [
            'url',
            'id',
            'cart',
            'person',
            'product',
            'product_variation_choices',
            'quantity',
            'price',
            'utilized',
            'permissions',
        ]
        extra_kwargs = {
            'product_variation_choices': {
                'allow_empty': True,
            },
            'utilized': {
                'read_only': True
            },
        }


class CartSerializer(HyperlinkedModelSerializer):
    holdings = HoldingSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = [
            'url',
            'id',
            'person',
            'purchased',
            'holdings'
        ]


class CartPurchaseSerializer(serializers.ModelSerializer):
    stripe_token = serializers.CharField(write_only=True)

    class Meta:
        model = Cart
        fields = [
            'stripe_token'
        ]

    def update(self, instance, validated_data):
        stripe_token = validated_data.pop('stripe_token')
        try:
            instance.purchase(stripe_token)
        except stripe.error.StripeError as e:
            logger.warning('', exc_info=True)
            raise exceptions.PaymentDenied()
        return instance


class ProductVariationChoiceSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = ProductVariationChoice
        fields = [
            'url',
            'id',
            'variation',
            'name',
            'delta_amount',
            'order'
        ]


class ProductVariationSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = ProductVariation
        fields = [
            'url',
            'id',
            'product',
            'name',
            'choices'
        ]
        expandable_fields = {
            'choices': ('tickle.products.serializers.ProductVariationChoiceSerializer', (), {'many': True})
        }


class _ProductVariationSerializer(ProductVariationSerializer):
    choices = ProductVariationChoiceSerializer(many=True)

    class Meta:
        model = ProductVariation
        fields = [
            'url',
            'id',
            'name',
            'choices'
        ]


class ProductModifierSerializer(serializers.ModelSerializer):
    condition = serializers.SerializerMethodField()

    class Meta:
        model = Modifier
        fields = [
            'condition',
            'delta_amount'
        ]

    def get_condition(self, obj):
        return '{}'.format(obj.condition_subclass)


class ProductSerializer(HyperlinkedModelSerializer):
    modifiers = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'url',
            'slug',
            'name',
            'main_event',
            'description',
            'price',
            'is_available',
            'personal_limit',
            'modifiers',
            'variations',
        ]
        expandable_fields = {
            'main_event': ('tickle.events.serializers.MainEventSerializer', (), {}),
            'variations': ('tickle.products.serializers.ProductVariationSerializer', (), {'many': True})
        }

    def get_person(self):
        return self.context['request'].user

    def get_modifiers(self, obj):
        modifiers = obj.modifiers.eligible(self.get_person()).select_related('condition')
        serializer = ProductModifierSerializer(modifiers, read_only=True, many=True)
        return serializer.data

    def get_is_available(self, obj):
        return obj.is_available
