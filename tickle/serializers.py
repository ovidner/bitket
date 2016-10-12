from __future__ import absolute_import, unicode_literals

import stripe
from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework import serializers
from tickle.products.serializers import logger

from tickle import exceptions
from tickle.models import MainEvent, Organizer, Person, StudentUnion, Holding, \
    Cart, ProductVariationChoice, ProductVariation, ProductModifier, Product
from tickle.routers import parent_lookups
from tickle.utils import get_double_underscore_attr


class HyperlinkedRelatedField(serializers.HyperlinkedRelatedField):
    def __init__(self, *args, **kwargs):
        self._parent_lookups = kwargs.pop('parent_lookups', {})
        super(HyperlinkedRelatedField, self).__init__(*args, **kwargs)

    def use_pk_only_optimization(self):
        # This just gives us a load of problems. Disabled for now.
        return False

    def get_parent_lookups(self):
        return self._parent_lookups

    def get_url(self, obj, view_name, request, format):
        """
        Given an object, return the URL that hyperlinks to the object.

        May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
        attributes are not configured to correctly match the URL conf.
        """
        # Unsaved objects will not yet have a valid URL.
        if hasattr(obj, 'pk') and obj.pk is None:
            return None

        lookup_value = getattr(obj, self.lookup_field)
        kwargs = {self.lookup_url_kwarg: lookup_value}

        for kwarg, orm_lookup in self.get_parent_lookups().iteritems():
            kwargs[kwarg] = get_double_underscore_attr(obj, orm_lookup)

        return self.reverse(view_name, kwargs=kwargs, request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        """
        Return the object corresponding to a matched URL.

        Takes the matched URL conf arguments, and should return an
        object instance, or raise an `ObjectDoesNotExist` exception.
        """
        lookup_value = view_kwargs[self.lookup_url_kwarg]
        lookup_kwargs = {self.lookup_field: lookup_value}

        for kwarg, orm_lookup in self.get_parent_lookups().iteritems():
            lookup_kwargs[orm_lookup] = view_kwargs[kwarg]

        return self.get_queryset().get(**lookup_kwargs)


class HyperlinkedIdentityField(HyperlinkedRelatedField):
    def __init__(self, view_name=None, **kwargs):
        assert view_name is not None, 'The `view_name` argument is required.'
        kwargs['read_only'] = True
        kwargs['source'] = '*'
        super(HyperlinkedIdentityField, self).__init__(view_name, **kwargs)


class HyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    serializer_url_field = HyperlinkedIdentityField
    serializer_related_field = HyperlinkedRelatedField


class MainEventSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = MainEvent
        fields = [
            'url',
            'slug',
            'name',
            'description'
        ]
        extra_kwargs = {
            'url': {
                'lookup_field': 'slug',
                'parent_lookups': parent_lookups.MAIN_EVENT
            }
        }


class OrganizerSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Organizer
        fields = [
            'url',
            'name',
            'slug'
        ]
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class PersonSerializer(HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    default_cart = HyperlinkedRelatedField(
        read_only=True,
        view_name='cart-detail')

    class Meta:
        model = Person
        fields = [
            'url',
            'id',
            'first_name',
            'last_name',
            'pid',
            'liu_id',
            'liu_card_rfid',
            'student_union',
            'password',
            'email',
            'default_cart'
        ]
        extra_kwargs = {
            'student_union': {'lookup_field': 'slug'}
        }


class StudentUnionSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = StudentUnion
        fields = [
            'url',
            'slug',
            'name'
        ]
        extra_kwargs = {
            'url': {
                'lookup_field': 'slug'
            }
        }


class HoldingSerializer(HyperlinkedModelSerializer):
    price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    product_name = serializers.SerializerMethodField()
    permissions = DRYPermissionsField(actions=['utilize', 'unutilize'])

    class Meta:
        model = Holding
        fields = [
            'url',
            'id',
            'cart',
            'person',
            'product',
            'product_name',  # Bluuh! fixme!
            'product_variation_choices',
            'quantity',
            'price',
            'purchase_price',
            'utilized',
            'permissions',
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

    def get_product_name(self, obj):
        return obj.product.name


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
