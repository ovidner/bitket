# -*- coding: utf-8 -*-
from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from invar.forms import BgMaxImportForm


class BgMaxImportView(FormView):
    form_class = BgMaxImportForm
    success_url = reverse_lazy('admin:invar_transaction_import_bgmax')

    def form_valid(self, form):
        form.save()

        messages.success(self.request, _('Successfully imported transactions from BgMax file.'))
        return super(BgMaxImportView, self).form_valid(form)
