# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import inlineformset_factory
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Div, HTML

from .models import Entry, EntryMaterial, EntryCustomMaterial, EntryType


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = [
            'constellation',
            'name',
            'entry_type',
            'members',
            'width',
            'length',
            'height',
            'description',
            'spex_description',
            'other_information',

            'primary_contact_name',
            'primary_contact_address',
            'primary_contact_postcode',
            'primary_contact_city',
            'primary_contact_phone',
            'primary_contact_email',
            'secondary_contact_name',
            'secondary_contact_address',
            'secondary_contact_postcode',
            'secondary_contact_city',
            'secondary_contact_phone',
            'secondary_contact_email',
        ]

    def clean(self):
        data = super(EntryForm, self).clean()

        if hasattr(data, 'entry_type'):
            # These validations break if entry_type isn't defined.
            if data['members'] > data['entry_type'].max_members:
                self.add_error('members', ValidationError(_('Too many members for this entry type.')))

            if data['entry_type'].name == "Fribygge" and not (data['width'] and data['length'] and data['height']):
                self.add_error('entry_type', ValidationError(_('Free build must have specified, valid dimensions.')))

        return data


class EntryFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(EntryFormHelper, self).__init__(*args, **kwargs)

        self.form_tag = False
        self.layout = Layout(
            Div(
                Div(
                    'constellation',
                    css_class='col-sm-6'
                ),
                Div(
                    'name',
                    css_class='col-sm-6'
                ),
                css_class='row'
            ),
            'members',
            'entry_type',
            Div(
                Div(
                    'width',
                    css_class='col-sm-4'
                ),
                Div(
                    'length',
                    css_class='col-sm-4'
                ),
                Div(
                    'height',
                    css_class='col-sm-4'
                ),
                css_class='row',
                css_id='dimensions'  # Used by JS to hide
            ),
            'description',
            'spex_description',
            'other_information',
            Div(
                Div(
                    HTML(
                        u"""<h3>Kontaktperson 1</h3>"""
                    ),
                    'primary_contact_name',
                    'primary_contact_address',
                    Div(
                        Div(
                            'primary_contact_postcode',
                            css_class='col-xs-4'
                        ),
                        Div(
                            'primary_contact_city',
                            css_class='col-xs-8'
                        ),
                        css_class='row'
                    ),
                    'primary_contact_phone',
                    'primary_contact_email',
                    css_class='col-sm-6'
                ),
                Div(
                    HTML(
                        u"""<h3>Kontaktperson 2</h3>"""
                    ),
                    'secondary_contact_name',
                    'secondary_contact_address',
                    Div(
                        Div(
                            'secondary_contact_postcode',
                            css_class='col-xs-4'
                        ),
                        Div(
                            'secondary_contact_city',
                            css_class='col-xs-8'
                        ),
                        css_class='row'
                    ),
                    'secondary_contact_phone',
                    'secondary_contact_email',
                    css_class='col-sm-6'
                ),
                css_class='row'
            ),
        )


class EntryMaterialFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(EntryMaterialFormSetHelper, self).__init__(*args, **kwargs)

        self.form_tag = False
        self.template = 'crispy/bootstrap3/table_inline_formset.html'