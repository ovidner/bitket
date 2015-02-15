# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import FormView
from django.contrib import messages

from fungus.models import ShiftRegistration
from fungus.forms import ChangeSelectedShiftsForm


class ShiftChangeView(FormView):
    form_class = ChangeSelectedShiftsForm
    template_name = 'fungus/change_selected_shift.html'
    model = ShiftRegistration
    success_url = '/admin/%s/%s/' % (model._meta.app_label, model._meta.model_name)

    def get(self, request, *args, **kwargs):
        selected = request.GET.get('ids')
        queryset = self.model.objects.filter(id__in=selected.split(','))
        form = self.form_class(initial={'shift_registration': queryset})
        context = dict(
            queryset=queryset,
            form=form,
            content_type=self.model._meta.verbose_name_plural.title(),
            list_description="Alla följande arbetspass kommer att bytas: ",
            form_description="Välj arbetspass att byta till.",
        )
        return render(request, self.template_name, context)

    def form_valid(self, form):
        shift = form.cleaned_data['shift']
        shift_registration = form.cleaned_data['shift_registration']
        rows_updated = shift_registration.update(shift=shift)
        if rows_updated == 1:
            model_name = self.model._meta.verbose_name
        else:
            model_name = self.model._meta.verbose_name_plural
        messages.add_message(self.request, messages.SUCCESS, u"%s %s ändrades." % (rows_updated, model_name))
        return super(ShiftChangeView, self).form_valid(form)
