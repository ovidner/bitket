# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from hashlib import sha1

from django.utils.translation import ungettext_lazy, ugettext_lazy as _
from django import forms

from invar.models import BgMaxImport, Transaction
from invar.utils.bgmax import parse_file


class _BgMaxImportModelForm(forms.ModelForm):
    class Meta:
        model = BgMaxImport
        fields = ('file_name', 'file_sha1', 'creation_timestamp')


class BgMaxImportForm(forms.Form):
    file = forms.FileField()

    parse_cache = None

    def clean_file(self):
        _file = self.cleaned_data['file']
        file_buffer = _file.read()

        self.parse_cache = parse_file(file_buffer)

        form = _BgMaxImportModelForm({
            'file_name': _file.name,
            'file_sha1': sha1(file_buffer).hexdigest(),
            'creation_timestamp': self.parse_cache['creation_timestamp'],
            })

        if form.is_valid():
            # we don't want to put the object to the database on this step
            self.instance = form.save(commit=False)
        else:
            raise forms.ValidationError(u"The file contains invalid data.")

        return _file

    def save_transactions(self):
        for section in self.parse_cache['sections']:
            for payment in section['payments']:
                Transaction.objects.create(timestamp=section['deposit_date'],
                                           amount=payment['amount'],
                                           reference=payment['reference'],
                                           uid=payment['uid'])

    def save(self):
        # We are not overriding the `save` method here because `form.Form` does not have it.
        # We just add it for convenience.
        instance = getattr(self, "instance", None)
        if instance:
            instance.save()
            self.save_transactions()

        return instance
