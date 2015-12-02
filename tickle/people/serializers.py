from __future__ import absolute_import, unicode_literals

from rest_framework import serializers

from tickle.common.routers import parent_lookups
from tickle.common.serializers import (HyperlinkedModelSerializer,
                                       HyperlinkedRelatedField)
from .models import Person, StudentUnion


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
