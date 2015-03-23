# -*- coding: utf-8 -*-
from django import forms
from django.db.models import Count, F, Q

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Div
from crispy_forms.bootstrap import InlineCheckboxes

from fungus.models import Shift, ShiftRegistration, Functionary


class ChangeSelectedShiftsForm(forms.Form):
    shift_registration = forms.ModelMultipleChoiceField(queryset=ShiftRegistration.objects.all(),
                                                        widget=forms.MultipleHiddenInput(), required=False)
    shift = forms.ModelChoiceField(queryset=Shift.objects.all(), empty_label=None, required=True)


class ShiftForm(forms.Form):
    shifts = forms.ModelMultipleChoiceField(label='', required=False, widget=forms.CheckboxSelectMultiple(),
                                           queryset=Shift.objects.registerable().order_by('shift_type', 'start'))

    def clean_shift(self):
        data = self.cleaned_data['shifts']
        if len(data) == 0:
            raise forms.ValidationError("You haven't chosen any shifts. You need to select at least one.")
        elif len(data) > 1:
            data = data.order_by('start')
            for i in range(0, len(data) - 1):
                if (data[i].start <= data[i + 1].end) and (data[i].end >= data[i + 1].start):
                    raise forms.ValidationError("You have chosen two shifts that overlap.")
        return data


class FunctionaryForm(forms.ModelForm):
    class Meta:
        model = Functionary
        fields = ('b_driving_license',)


class ShiftRegisterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ShiftRegisterFormHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.layout = Layout()


class FunctionaryFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(FunctionaryFormHelper, self).__init__(*args, **kwargs)

        self.form_tag = False
        self.layout = Layout(
            Div(
                Div(
                    'ice_number',
                    css_class='col-sm-6'
                ),
                Div(
                    'b_driving_license',
                    css_class='col-sm-6'
                ),
                css_class='row'
            ),

        )
