# -*- coding: utf-8 -*-
from django import forms
from django.db.models import Count, F, Q

from crispy_forms.helper import FormHelper, Layout

from fungus.models import Shift, ShiftRegistration


class ChangeSelectedShiftsForm(forms.Form):
    shift_registration = forms.ModelMultipleChoiceField(queryset=ShiftRegistration.objects.all(),
                                                        widget=forms.MultipleHiddenInput(), required=False)
    shift = forms.ModelChoiceField(queryset=Shift.objects.all(), empty_label=None, required=True)


class ShiftRegisterForm(forms.Form):
    shift = forms.ModelMultipleChoiceField(label='', required=False, widget=forms.CheckboxSelectMultiple(),
                                           queryset=Shift.objects.annotate(registranion_count=Count('registrations'))
                                           .filter(Q(public=True) & (Q(people_max__isnull=True) |
                                                                     Q(registranion_count__lt=F('people_max'))))
                                           .order_by('shift_type'))
    accept_terms = forms.BooleanField(label='Jag har förstått bla bla bla...', required=True)


class ShiftRegisterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ShiftRegisterFormHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.layout = Layout('accept_terms')
