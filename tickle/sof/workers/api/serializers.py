# -*- coding: utf-8 -*-
from rest_framework import serializers

from fungus.models import Shift, ShiftRegistration


class ShiftSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shift
        fields = ('start', 'end',)


class ShiftRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftRegistration
        fields = ('shift', 'person', 'checked_in', 'checked_out')
