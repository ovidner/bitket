# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.validators import EMPTY_VALUES

from localflavor.se.forms import SWEDISH_ID_NUMBER
from localflavor.se.utils import validate_id_birthday, id_number_checksum
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Div
from crispy_forms.bootstrap import InlineCheckboxes

from tickle.models import Person, Holding, Product


class PublicNameModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.public_name


class SEPersonalIdentityNumberField(forms.CharField):
    """
    A form field that validates input as a Swedish personal identity number
    (personnummer).

    The correct formats are YYYYMMDD-XXXX, YYYYMMDDXXXX, YYMMDD-XXXX,
    YYMMDDXXXX and YYMMDD+XXXX. XXXX can be 0000.

    A + indicates that the person is older than 100 years, which will be taken
    into consideration when the date is validated.

    The birth date is checked to be a valid date.

    By default, co-ordination numbers (samordningsnummer) will be accepted. To
    only allow real personal identity numbers, pass the keyword argument
    coordination_number=False to the constructor.

    Returns (date, code) where date is a datetime.date object and code is a string with the last four characters or None
    if input was YYMMDD-0000.
    """

    def __init__(self, coordination_number=True, *args, **kwargs):
        self.coordination_number = coordination_number
        super(SEPersonalIdentityNumberField, self).__init__(*args, **kwargs)

    default_error_messages = {
        'invalid': _('Enter a valid Swedish personal identity number or YYMMDD-0000.'),
        'coordination_number': _('Co-ordination numbers are not allowed.'),
        }

    def clean(self, value):
        value = super(SEPersonalIdentityNumberField, self).clean(value)

        if value in EMPTY_VALUES:
            return None, None

        match = SWEDISH_ID_NUMBER.match(value)
        if match is None:
            raise forms.ValidationError(self.error_messages['invalid'])

        gd = match.groupdict()

        code = str(gd['serial'] + gd['checksum'])

        # compare the calculated value with the checksum
        # if id_number_checksum(gd) != int(gd['checksum']):
        #     raise forms.ValidationError(self.error_messages['invalid'])

        # check for valid birthday
        try:
            birth_day = validate_id_birthday(gd)
        except ValueError:
            raise forms.ValidationError(self.error_messages['invalid'])

        # make sure that co-ordination numbers do not pass if not allowed
        if not self.coordination_number and int(gd['day']) > 60:
            raise forms.ValidationError(self.error_messages['coordination_number'])

        if code == '0000':
            return birth_day, None

        return birth_day, code


class AcceptForm(forms.Form):
    accept = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput,
        label=_('I accept that my personal information will be stored'),
        help_text=_('We store your personal information according to the regulations specified by the Swedish Personal Data Act (PUL) and will not share it with any third parties.')
    )


class PersonForm(forms.ModelForm):
    phone = forms.CharField(required=True, label=_('Phone number'))
    pid = SEPersonalIdentityNumberField(coordination_number=True, label=_('Personal identity number'), help_text=_("Swedish personal identity number in the format <em>YYMMDD-XXXX</em>. If you don't have one, enter <em>YYMMDD-0000</em>, where <em>YYMMDD</em> represents your birthday."))

    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'pid', 'phone', 'email', 'special_nutrition', 'notes')
        widgets = {
            'special_nutrition': forms.CheckboxSelectMultiple,  # TODO: Better multi-select solution.
        }

    def save(self, commit=True):
        birth_date, pid_code = self.cleaned_data['pid']

        self.instance.birth_date = birth_date
        self.instance.pid_code = pid_code

        return super(PersonForm, self).save(commit=commit)

    def clean(self):
        data = super(PersonForm, self).clean()

        birth_date, pid_code = self.cleaned_data['pid']

        # Checks for PID collision
        if birth_date and pid_code and self._meta.model.objects.filter(birth_date=birth_date, pid_code=pid_code).exists():
            self.add_error('pid', forms.ValidationError(_('This personal identity number is already registered. Please contact us if you think this is a mistake.')))

        return data


class PersonFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(PersonFormHelper, self).__init__(*args, **kwargs)

        self.form_tag = False
        self.layout = Layout(
            Div(
                Div(
                    'first_name',
                    css_class='col-sm-6'
                ),
                Div(
                    'last_name',
                    css_class='col-sm-6'
                ),
                css_class='row'
            ),
            Div(
                Div(
                    'phone',
                    css_class='col-sm-6'
                ),
                Div(
                    'email',
                    css_class='col-sm-6'
                ),
                css_class='row'
            ),
            Div(
                Div(
                    'pid',
                    css_class='col-sm-6'
                ),
                Div(
                    css_class='col-sm-6'
                ),
                css_class='row'
            ),
            Div(
                Div(
                    InlineCheckboxes('special_nutrition'),
                    css_class='col-sm-12'
                ),
                css_class='row'
            ),

            'notes'
        )


class AcceptFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(AcceptFormHelper, self).__init__(*args, **kwargs)

        self.form_tag = False
        self.layout = Layout(
            'accept'
        )