# -*- coding: utf-8 -*-
from django import forms

from tickle.models import Person, Holding, Product


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'id_number', 'phone', 'email', 'special_nutrition', 'notes')
        widgets = {
            'special_nutrition': forms.CheckboxSelectMultiple,  # TODO: Better multi-select solution.
        }

