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

from tickle.models import Person, Product, Holding, ShoppingCart, Delivery
from tickle.fields import SEPersonalIdentityNumberField, LiUIDField


class TurboDeliveryForm(forms.Form):
    liu_card_rfid = forms.CharField(required=False, label=_('RFID card number'))
    pid = SEPersonalIdentityNumberField(required=False, label=_('Personal identity number'))

    auto_products = forms.ModelMultipleChoiceField(queryset=Product.objects.all(), label=_('Auto deliver products'))

    def clean(self):
        data = super(TurboDeliveryForm, self).clean()

        if not data.get('liu_card_rfid') and data.get('pid') == (None, None, False):
            msg = _('Must supply RFID number or PID.')
            self.add_error('liu_card_rfid', msg)
            self.add_error('pid', msg)

        return data

    def get_person(self):
        liu_card_rfid = self.cleaned_data['liu_card_rfid']
        pid = self.cleaned_data['pid']

        if liu_card_rfid:
            get_kwargs = {'liu_card_rfid': liu_card_rfid}
        else:
            get_kwargs = {'birth_date': pid[0], 'pid_code': pid[1], 'pid_coordination': pid[2]}

        return Person.objects.get(**get_kwargs)

    def get_auto_holdings(self):
        return Holding.objects.filter(person=self.get_person(), product__in=self.cleaned_data['auto_products'])

    def deliver_auto_holdings(self):
        holdings = self.get_auto_holdings().deliverable()

        if holdings:
            delivery = Delivery.objects.create()
            delivery.holdings = self.get_auto_holdings().deliverable()
        else:
            delivery = None

        return delivery


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


class SimplePersonForm(forms.ModelForm):
    pid = SEPersonalIdentityNumberField(coordination_number=True, interim_number=True,
                                        label=_('Personal identity number'),
                                        help_text=_("Swedish personal identity number in the format "
                                                    "<em>YYMMDD-XXXX</em>. If you don't have one, enter "
                                                    "<em>YYMMDD-0000</em>, where <em>YYMMDD</em> represents your "
                                                    "birthday."))

    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'pid', 'email',)

    def save(self, commit=True):
        birth_date, pid_code, pid_coordination = self.cleaned_data['pid']

        self.instance.birth_date = birth_date
        self.instance.pid_code = pid_code
        self.instance.pid_coordination = pid_coordination

        return super(SimplePersonForm, self).save(commit=commit)

    def clean(self):
        data = super(SimplePersonForm, self).clean()

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


class PersonForm(SimplePersonForm):
    phone = forms.CharField(required=True, label=_('Phone number'))

    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'pid', 'phone', 'email', 'special_nutrition', 'notes')
        widgets = {
            'special_nutrition': forms.CheckboxSelectMultiple,  # TODO: Better multi-select solution.
        }


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


class SimplePersonFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(SimplePersonFormHelper, self).__init__(*args, **kwargs)

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
                    'pid',
                    css_class='col-sm-6'
                ),
                Div(
                    'email',
                    css_class='col-sm-6'
                ),
                css_class='row'
            ),
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


class IdentifyForm(forms.Form):
    liu_id = LiUIDField(employee_id=True, student_id=True, label=_('LiU ID'), required=False)
    pid = SEPersonalIdentityNumberField(coordination_number=True, label=_('Personal identity number'), help_text=_(
        "Swedish personal identity number in the format <em>YYMMDD-XXXX</em>. If you don't have one, "
        "enter <em>YYMMDD-0000</em>, where <em>YYMMDD</em> represents your birthday."), required=False)

    def __init__(self, *args, **kwargs):
        super(IdentifyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True

    def clean(self):
        data = super(IdentifyForm, self).clean()
        # XOR
        if bool(data.get('liu_id', None)) == bool(data.get('pid', (None, None, False))[0]):
            raise ValidationError(_('Please specify LiU ID or personal identity number.'))

        return data

    def get_existing_person_or_none(self):
        try:
            liu_id = self.cleaned_data['liu_id']
            if liu_id:
                return Person.objects.get(liu_id__exact=liu_id)
            else:
                pid = self.cleaned_data['pid']
                return Person.objects.get(birth_date__exact=pid[0], pid_code__exact=pid[1])
        except Person.DoesNotExist:
            return None


class AddProductToShoppingCartForm(forms.ModelForm):
    people = forms.ModelMultipleChoiceField(queryset=Person.objects.all(), widget=forms.MultipleHiddenInput())
    product = forms.ModelChoiceField(queryset=Product.objects.all(), empty_label=None, required=True)

    class Meta:
        model = Holding

        fields = ('people', 'product', 'quantity', '_transferable')

    def save(self, commit=True):
        product = self.cleaned_data['product']
        quantity = self.cleaned_data['quantity']
        _transferable = self.cleaned_data['_transferable']

        for person in self.cleaned_data['people']:
            shopping_cart, shopping_cart_created = ShoppingCart.objects.get_or_create(person=person)

            Holding.objects.get_or_create(
                person=person,
                product=product,
                defaults={'shopping_cart': shopping_cart,
                          'quantity': quantity,
                          '_transferable': _transferable}
            )
