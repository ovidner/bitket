# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.forms.widgets import flatatt
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthenticationForm

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Div
from crispy_forms.bootstrap import InlineCheckboxes

from tickle.models import Person
from tickle.fields import SEPersonalIdentityNumberField, LiUIDField


class AcceptForm(forms.Form):
    accept = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput,
        label=_('I accept that my personal information will be stored'),
        help_text=_(
            'We store your personal information according to the regulations specified by the Swedish Personal Data '
            'Act (PUL) and will not share it with any third parties.')
    )


class LiUIDOrEmailForm(forms.Form):
    liu_id = LiUIDField(employee_id=True, student_id=True, label=_('LiU ID'))
    email = forms.EmailField()

    def clean(self):
        data = super(LiUIDOrEmailForm, self).clean()

        # XOR
        if bool(data['liu_id']) != bool(data['email']):
            raise ValidationError(_('Please specify LiU ID <em>or</em> email address.'))

        return data

    def get_existing_person(self):
        return Person.objects.get(
            Q(liu_id__exact=self.cleaned_data['liu_id']) |
            Q(email__exact=self.cleaned_data['email']))


class AuthenticationForm(DjangoAuthenticationForm):
    username = forms.CharField(max_length=254, label=_('LiU ID or email address'))


class PersonForm(forms.ModelForm):
    phone = forms.CharField(required=True, label=_('Phone number'))
    pid = SEPersonalIdentityNumberField(coordination_number=True, interim_number=True,
                                        label=_('Personal identity number'),
                                        help_text=_("Swedish personal identity number in the format "
                                                    "<em>YYMMDD-XXXX</em>. If you don't have one, enter "
                                                    "<em>YYMMDD-0000</em>, where <em>YYMMDD</em> represents your "
                                                    "birthday."))

    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'pid', 'phone', 'email', 'special_nutrition', 'notes')
        widgets = {
            'special_nutrition': forms.CheckboxSelectMultiple,  # TODO: Better multi-select solution.
        }

    def save(self, commit=True):
        birth_date, pid_code, pid_coordination = self.cleaned_data['pid']

        self.instance.birth_date = birth_date
        self.instance.pid_code = pid_code
        self.instance.pid_coordination = pid_coordination

        return super(PersonForm, self).save(commit=commit)

    def clean(self):
        data = super(PersonForm, self).clean()

        try:
            # pid consists of None when invalid
            birth_date, pid_code, pid_coordination = data['pid']

            # Checks for PID collision
            if birth_date and pid_code and self._meta.model.objects.filter(birth_date=birth_date,
                                                                           pid_code=pid_code,
                                                                           pid_coordination=pid_coordination).exists():
                self.add_error('pid', forms.ValidationError(_(
                    'This personal identity number is already registered. Please contact us if you think this is a '
                    'mistake.')))
        except KeyError:
            # self.add_error('pid', forms.ValidationError(_('Enter a valid Swedish personal identity number.')))
            pass

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


class LoginFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(LoginFormHelper, self).__init__(*args, **kwargs)

        self.form_tag = False


class ChangePasswordFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordFormHelper, self).__init__(*args, **kwargs)

        self.form_tag = False


class DisplayWidget(forms.Widget):
    """ Widget for only displaying a value in a form. """

    def __init__(self, attrs=None):
        super(DisplayWidget, self).__init__(attrs)
        self.initial_attrs = self.attrs.copy()

    def render(self, name, value, attrs=None):
        self.attrs = self.initial_attrs  # Removes crispy forms css, DisplayWidget should not look like form input.
        final_attrs = self.build_attrs(attrs, name=name)
        return mark_safe(u'<span %s>%s</span>' % (flatatt(final_attrs), escape(value) or ''))


class DisplayField(forms.Field):
    """ Form field for only displaying a read-only field. """
    widget = DisplayWidget

    def __init__(self, display_value=None, *args, **kwargs):
        super(DisplayField, self).__init__(*args, **kwargs)
        self.required = False
        self.display_value = display_value

    def prepare_value(self, value):
        if self.display_value is not None:
            value = self.display_value
        return value

    def clean(self, value):
        return self.initial

    def has_changed(self, initial, data):
        return False
