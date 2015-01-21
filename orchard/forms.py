# -*- coding: utf-8 -*-
from django import forms
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Div, HTML, Field
from crispy_forms.bootstrap import InlineCheckboxes, AppendedText

from tickle.models.people import Person
from tickle.models.products import Purchase, Holding, Product
from tickle.forms import PersonForm, PublicNameModelChoiceField
from orchard.models import Orchestra, OrchestraMembership, OrchestraTicketType, OrchestraProduct


class OrchestraStuffForm(forms.ModelForm):
    product = PublicNameModelChoiceField(queryset=OrchestraProduct.objects.all(), widget=forms.HiddenInput, label=_('Product'))  # todo: filter this
    quantity = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Holding
        fields = ['product', 'quantity']


class RadioInput(forms.CheckboxInput):
    """ Custom hardcoded class for a simple radio button input used in formsets. """

    def render(self, name, value, attrs=None):
        if name.startswith('orchestra_memberships-0'):
            return mark_safe(u'<input type="radio" name="primary" value="%s" checked />' % name)
        return mark_safe(u'<input type="radio" name="primary" value="%s" />' % name)

    def value_from_datadict(self, data, files, name):
        value = data.get('primary')
        return bool(name == value)


class OrchestraMembershipForm(forms.ModelForm):
    class Meta:
        model = OrchestraMembership
        fields = ['orchestra', 'primary']
        widgets = {
            'primary': RadioInput,  # TODO: Better multi-select solution.
        }


class DisplayWidget(forms.Widget):
    """ Widget for only displaying a value in a form. """
    def render(self, name, value, attrs=None):
        # final_attrs = self.build_attrs(attrs, name=name)
        if hasattr(self, 'initial'):
            if isinstance(self.initial, bool):
                value = self.initial and 'Ja' or 'Nej'
            else:
                value = self.initial.full_name
        # return mark_safe("<span %s>%s</span>" % (flatatt(final_attrs), escape(value) or ''))
        return mark_safe(escape(value) or '')

    def _has_changed(self, initial, data):
        return False


class DisplayField(forms.Field):
    """ Form field for only displaying a read-only field. """
    widget = DisplayWidget

    def __init__(self, *args, **kwargs):
        super(DisplayField, self).__init__(*args, **kwargs)
        self.widget.initial = self.initial

    def clean(self, value):
        return self.widget.initial


class OrchestraMembershipApprovalForm(forms.ModelForm):
    # approved = forms.ChoiceField(widget=forms.RadioSelect(), choices=((True, 'Ja',), (False, 'Nej')), )
    approved = forms.BooleanField(label='Godkänd', required=False)

    class Meta:
        model = OrchestraMembership
        fields = ['person', 'primary', 'approved']

    def __init__(self, *args, **kwargs):
        super(OrchestraMembershipApprovalForm, self).__init__(*args, **kwargs)
        # Set initial values for display fields to the correct instance of OrchestraMembership.
        self.fields['person'] = DisplayField(initial=self.instance.person, required=False)
        self.fields['primary'] = DisplayField(initial=self.instance.primary, required=False, label='Primär')


class OrchestraTicketTypePublicNameModelChoiceField(forms.ModelChoiceField):
    """
    At least we're explicit with the class name...
    """
    def label_from_instance(self, obj):
        return obj.ticket_type.public_name


class OrchestraMemberRegistrationForm(forms.Form):
    ticket_type = OrchestraTicketTypePublicNameModelChoiceField(queryset=OrchestraTicketType.objects.all(), label=_('Ticket type'))
    food = forms.BooleanField(widget=forms.CheckboxInput, required=False, label=_('Food'), help_text=_('Meals as described above.'))
    accommodation = forms.BooleanField(widget=forms.CheckboxInput, required=False, label=_('Accommodation'), help_text=_('Place on floor &ndash; bring your own bedroll. Breakfast included.'))
    dinner = forms.BooleanField(widget=forms.CheckboxInput, required=False, label=_("10-/25-year dinner"), help_text=_('Doing your 10th SOF/STORK in a row or the 25th in all? Go to the party!'))

    def clean(self):
        data = super(OrchestraMemberRegistrationForm, self).clean()

        if data['food'] and not data['ticket_type'].food_ticket_type:
            self.add_error('food', ValidationError(_("Can't add food to this ticket type.")))

        if data['accommodation'] and not data['ticket_type'].accommodation_ticket_type:
            self.add_error('accommodation', ValidationError(_("Can't add accommodation to this ticket type.")))

        if data['dinner'] and not data['ticket_type'].dinner_ticket_type:
            self.add_error('dinner', ValidationError(_("Can't add 10-/25-year dinner to this ticket type.")))

        return data


class ApproveOrchestraMemberForm(forms.ModelForm):
    class Meta:
        model = Orchestra
        fields = []


class OrchestraTicketFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(OrchestraTicketFormHelper, self).__init__(*args, **kwargs)

        self.form_tag = False
        self.layout = Layout(
            'ticket_type',
            'food',
            'accommodation',
            'dinner',
        )


class InlineFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(InlineFormSetHelper, self).__init__(*args, **kwargs)

        self.form_tag = False
        self.template = 'crispy/bootstrap3/table_inline_formset.html'