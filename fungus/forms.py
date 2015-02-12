# -*- coding: utf-8 -*-
from django import forms
from fungus.models import Shift, ShiftRegistration


class ChangeSelectedShiftsForm(forms.Form):
    shift_registration = forms.ModelMultipleChoiceField(queryset=ShiftRegistration.objects.all(),
                                                        widget=forms.MultipleHiddenInput(), required=False)
    shift = forms.ModelChoiceField(queryset=Shift.objects.all(), empty_label=None, required=True)