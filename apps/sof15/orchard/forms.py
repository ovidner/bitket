# -*- coding: utf-8 -*-
from django import forms
from django.utils.safestring import mark_safe

from orchard.models import Orchestra


class RadioInput(forms.CheckboxInput):
    """ Custom hardcoded class for a simple radio button input used in formsets. """

    def render(self, name, value, attrs=None):
        if name.startswith('form-0'):
            return mark_safe(u'<input type="radio" name="primary" value="%s" checked />' % name)
        return mark_safe(u'<input type="radio" name="primary" value="%s" />' % name)

    def value_from_datadict(self, data, files, name):
        value = data.get('primary')
        return bool(name == value)


class SOF15OrchestraMemberRegistrationForm(forms.Form):
    orchestra = forms.ModelChoiceField(queryset=Orchestra.objects, label='')
    active = forms.BooleanField(required=False, label='')
    primary = forms.BooleanField(widget=RadioInput, required=False)
