from __future__ import absolute_import, unicode_literals
import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
import stripe

from tickle.common import exceptions
from tickle.common.routers import parent_lookups
from tickle.common.serializers import HyperlinkedModelSerializer, HyperlinkedRelatedField
from tickle.events.models import MainEvent
from tickle.modifiers.models import ProductModifier
from .models import Cart, Holding, Product, ProductVariation, ProductVariationChoice


class HoldingSerializer(HyperlinkedModelSerializer):
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
            'utilized',
            'purchase_price'
        ]
        extra_kwargs = {
            'product': {
                'lookup_field': 'slug',
                'parent_lookups': parent_lookups.PRODUCT
            },
            'product_variation_choices': {
                'allow_empty': True,
                'parent_lookups': parent_lookups.PRODUCT_VARIATION_CHOICE
            },
            'utilized': {
                'read_only': True
            },
            'purchase_price': {
                'read_only': True
            }
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
        except stripe.error.StripeError:
            logger.warning('', exc_info=True)
            raise exceptions.PaymentDenied()
        return instance


class ProductVariationChoiceSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = ProductVariationChoice
        fields = [
            'url',
            'id',
            'name',
            'delta_amount'
        ]
        extra_kwargs = {
            'url': {
                'parent_lookups': parent_lookups.PRODUCT_VARIATION_CHOICE
            }
        }


class ProductVariationSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = ProductVariation
        fields = [
            'url',
            'id',
            'name'
        ]
        extra_kwargs = {
            'url': {
                'parent_lookups': parent_lookups.PRODUCT_VARIATION
            }
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
        extra_kwargs = {
            'url': {
                'parent_lookups': parent_lookups.PRODUCT_VARIATION
            }
        }


class ProductModifierSerializer(serializers.ModelSerializer):
    condition = serializers.SerializerMethodField()

    class Meta:
        model = ProductModifier
        fields = [
            'condition',
            'delta_amount'
        ]

    def get_condition(self, obj):
        return '{}'.format(obj.condition_subclass)


class ProductSerializer(HyperlinkedModelSerializer):
    modifiers = serializers.SerializerMethodField()
    variations = _ProductVariationSerializer(many=True)
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'url',
            'slug',
            'name',
            'description',
            'base_price',
            'is_available',
            'personal_limit',
            'modifiers',
            'variations',
        ]
        extra_kwargs = {
            'url': {
                'lookup_field': 'slug',
                'parent_lookups': parent_lookups.PRODUCT
            }
        }

    def get_person(self):
        return self.context['request'].user

    def get_modifiers(self, obj):
        modifiers = obj.product_modifiers.eligible(self.get_person()).select_related('condition')
        serializer = ProductModifierSerializer(modifiers, read_only=True, many=True)
        return serializer.data

    def get_is_available(self, obj):
        return obj.is_available
