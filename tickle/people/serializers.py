from __future__ import absolute_import, unicode_literals

from rest_framework import serializers

from tickle.common.routers import parent_lookups
from tickle.common.serializers import (HyperlinkedModelSerializer,
                                       HyperlinkedRelatedField)
from .models import Person, StudentUnion


class PersonSerializer(HyperlinkedModelSerializer):
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
            'email',
            'carts'
        ]


class StudentUnionSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = StudentUnion
        fields = [
            'url',
            'id',
            'slug',
            'name'
        ]
