# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.forms import CheckboxSelectMultiple


from tickle.models import Person, Holding


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'id_number', 'phone', 'email', 'special_nutrition', 'notes')
        widgets = {
            'special_nutrition': CheckboxSelectMultiple,  # TODO: Better multi-select solution.
        }
