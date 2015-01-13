# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.forms import CheckboxSelectMultiple

from tickle.models import Person


class SOF15PersonRegistrationForm(ModelForm):
    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'id_number', 'email', 'special_nutrition')
        widgets = {
            'special_nutrition': CheckboxSelectMultiple,  # TODO: Better multi-select solution.
        }